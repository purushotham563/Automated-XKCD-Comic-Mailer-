# 📬 XKCD Comic Mailer

This project automates the process of downloading XKCD comics from the previous month and sending them via email as attachments. It runs monthly using a scheduler, leveraging web scraping, multithreading, and SMTP email delivery.

---

## 🚀 Features

- Automatically scrapes XKCD comics for the entire previous month
- Downloads comics using multithreaded requests for efficiency
- Sends comics as email attachments via Gmail SMTP
- Fully automated using Python’s `schedule` module
- Creates and organizes image files in a local `xkcd/` directory

---

## 🧰 Tech Stack

- **Language**: Python
- **Libraries**:
  - `requests` – HTTP requests
  - `bs4` (BeautifulSoup) – HTML parsing
  - `threading` – Concurrent downloads
  - `smtplib`, `email.mime` – Email sending with attachments
  - `schedule` – Monthly job automation
  - `datetime`, `calendar`, `os` – Time and file operations

---

## 🛠️ How It Works

1. **Get Latest XKCD Comic Number**:
   - Extracts the latest comic number from the homepage using meta tags.

2. **Determine Previous Month Range**:
   - Calculates number of days in the previous month to decide which comics to fetch.

3. **Download Comics Concurrently**:
   - Spawns a thread per comic number to scrape and save images locally in `/xkcd`.

4. **Compose and Send Email**:
   - Attaches all comics from the month and sends them via Gmail SMTP using a secure app password.

5. **Schedule Monthly Run**:
   - Configured to automatically run the script every month at 09:00 AM.

---

## 🧪 Sample Output

```
Downloading page https://xkcd.com/2852
Downloading image https://imgs.xkcd.com/comics/...
Image saved to xkcd/2852_comic.png
...
Email sent successfully
```

---

## 🔐 Security Note

> ⚠️ This script uses a Gmail App Password for authentication. Always use environment variables or secret managers to protect sensitive information. Do **not** commit credentials to your repository.

---

## 📧 Configuration

Update the following fields in the script:

```python
from_email = "your_email@gmail.com"
from_password = "your_gmail_app_password"
to_email = "receiver_email@example.com"
```

You must enable [App Passwords](https://support.google.com/accounts/answer/185833?hl=en) in your Google account.

---

## 📅 Scheduling

The script uses the `schedule` library:
```python
schedule.every().month.at("09:00").do(job)
```

Run it in a long-running environment (e.g., cloud VM, cron, or Raspberry Pi) to keep the scheduler alive.

---

## 📂 Project Structure

```
xkcd-comic-mailer/
│
├── xkcd/                  # Downloaded comics
├── comic_mailer.py        # Main script
└── README.md              # Project documentation
```

---

## 📌 Improvements for Future

- Dockerize for deployment
- Web UI to configure recipients
- Support multiple email providers (Outlook, SMTP2Go)
- Store sent logs in a database (e.g., SQLite)

---

## 🏁 Author

- **Purushotham Reddy**
- GitHub: [purushotham563](https://github.com/purushotham563)
