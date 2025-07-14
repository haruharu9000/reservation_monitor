import hashlib
import requests
import smtplib
from email.message import EmailMessage
import os

# 設定
URL = "https://24120801book-commerce-app-haruharu9000s-projects.vercel.app/"  # ←監視したいURLに変更！
# ←あなたのMacの絶対パスに合わせて！
HASH_FILE = "/Users/haruaki/reservation_monitor/monitor/last_hash.txt"
EMAIL_FROM = "nitori4baime@gmail.com"
EMAIL_TO = "nitori4baime@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "nitori4baime@gmail.com"
SMTP_PASSWORD = "juwg zwcj piro pxdd"


def get_page_hash(url):
    res = requests.get(url, timeout=10)
    content = res.text.encode("utf-8")
    return hashlib.sha256(content).hexdigest()


def read_last_hash(path):
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        return f.read().strip()


def write_hash(path, hash_value):
    with open(path, "w") as f:
        f.write(hash_value)


def send_email(subject, body):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO
    msg.set_content(body)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)


def main():
    try:
        current_hash = get_page_hash(URL)
        last_hash = read_last_hash(HASH_FILE)

        if current_hash != last_hash:
            print("ページが更新されました！")
            send_email("【予約ページ更新】", f"更新されたよ！\n{URL}")
            write_hash(HASH_FILE, current_hash)
        else:
            print("変更なし")
    except Exception as e:
        print("エラー:", e)


if __name__ == "__main__":
    main()
