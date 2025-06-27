import requests, os, bs4, threading, smtplib, schedule, time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import calendar
from datetime import datetime, timedelta

os.makedirs('xkcd', exist_ok=True)

downloaded_images = {}
def get_latest_comic_number():
    url = 'https://xkcd.com'
    res = requests.get(url)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    # Find the meta tag with property "og:url"
    meta_tag = soup.find('meta', property='og:url')
    if meta_tag and 'content' in meta_tag.attrs:
        comic_url = meta_tag['content']
        comic_number = int(comic_url.rstrip('/').split('/')[-1])
        return comic_number
    else:
        raise ValueError("Could not find the comic number in the page metadata.")

def get_previous_month_days():
    current_date = datetime.now()
    first_of_current_month = current_date.replace(day=1)
    last_of_previous_month = first_of_current_month - timedelta(days=1)
    days_in_previous_month = last_of_previous_month.day
    previous_month = last_of_previous_month.month
    previous_year = last_of_previous_month.year

    return days_in_previous_month, previous_month, previous_year

def downloadXkcd(comic_number):
    global downloaded_images
    try:
        print(f"Downloading page https://xkcd.com/{comic_number}")
        res = requests.get(f'https://xkcd.com/{comic_number}')
        res.raise_for_status()

        soup = bs4.BeautifulSoup(res.text, 'html.parser')
        comicElem = soup.select('#comic img')
        if comicElem == []:
            print(f'Could not find comic image for {comic_number}.')
            return

        comicUrl = comicElem[0].get('src')
        if not comicUrl.startswith('http'):
            comicUrl = 'https:' + comicUrl

        # Download the image
        print(f'Downloading image {comicUrl}...')
        res = requests.get(comicUrl)
        res.raise_for_status()

        image_path = os.path.join('xkcd', f'{comic_number}_{os.path.basename(comicUrl)}')
        with open(image_path, 'wb') as imageFile:
            for chunk in res.iter_content(100000):
                imageFile.write(chunk)

        downloaded_images[comic_number] = image_path
        print(f'Image saved to {image_path}')
    except Exception as e:
        print(f"Failed to download comic {comic_number}. Error: {e}")

def send_email(subject, body, to_email):
    from_email = "appireddyappi0@gmail.com"
    from_password = "nudh zsum vvsi dnqz"

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    for comic_number in sorted(downloaded_images.keys()):
        file_path = downloaded_images[comic_number]
        with open(file_path, 'rb') as file:
            attachment = MIMEBase('application', 'octet-stream')
            attachment.set_payload(file.read())
        encoders.encode_base64(attachment)
        attachment.add_header('Content-Disposition', f'attachment; filename={os.path.basename(file_path)}')
        msg.attach(attachment)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, from_password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email. Error: {str(e)}")

def job():
    global downloaded_images
    downloaded_images = {}

    current_comic_number = get_latest_comic_number()

    days_in_previous_month, month, year = get_previous_month_days()

    start_comic = current_comic_number - days_in_previous_month

    downloadThreads = []
    for i in range(start_comic, current_comic_number):
        downloadThread = threading.Thread(target=downloadXkcd, args=(i,))
        downloadThreads.append(downloadThread)
        downloadThread.start()

    for downloadThread in downloadThreads:
        downloadThread.join()

    print("Downloading done")

    subject = f"XKCD Comics for {calendar.month_name[month]} {year}"
    body = f"Here are the comics from the previous month ({calendar.month_name[month]} {year})!"

    to_email = "purushotham.appireddy@gmail.com"
    send_email(subject, body, to_email)

schedule.every().month.at("09:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
