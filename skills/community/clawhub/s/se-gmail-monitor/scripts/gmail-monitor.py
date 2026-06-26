#!/usr/bin/env python3
"""Boris Gmail Monitor - Read, send, and manage emails"""
import imaplib, smtplib, email as email_lib, sys, json
from email.header import decode_header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

CONFIG = json.load(open('/Users/your-agent/.openclaw/workspace/.gmail-config.json'))

def get_connection(account='info'):
    acc = CONFIG['accounts'][account]
    mail = imaplib.IMAP4_SSL(CONFIG['imap_server'])
    mail.login(acc['email'], acc['app_password'])
    return mail

def check_unread(account='info'):
    mail = get_connection(account)
    mail.select('inbox')
    _, msgs = mail.search(None, 'UNSEEN')
    unread = msgs[0].split()
    print(f"📬 {CONFIG['accounts'][account]['email']}: {len(unread)} unread emails")
    mail.logout()
    return len(unread)

def list_emails(account='info', count=10, folder='inbox'):
    mail = get_connection(account)
    mail.select(folder)
    _, msgs = mail.search(None, 'ALL')
    ids = msgs[0].split()
    latest = ids[-count:] if len(ids) >= count else ids
    
    for mid in reversed(latest):
        _, data = mail.fetch(mid, '(RFC822)')
        for part in data:
            if isinstance(part, tuple):
                msg = email_lib.message_from_bytes(part[1])
                subj = decode_header(msg['Subject'] or '')[0][0]
                if isinstance(subj, bytes): subj = subj.decode(errors='replace')
                print(f"From: {msg.get('From','')[:70]}")
                print(f"Subject: {subj[:100]}")
                print(f"Date: {msg.get('Date','')[:30]}")
                print()
    mail.logout()

def send_email(to, subject, body, account='boris'):
    acc = CONFIG['accounts'][account]
    msg = MIMEMultipart()
    msg['From'] = acc['email']
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    with smtplib.SMTP(CONFIG['smtp_server'], CONFIG['smtp_port']) as server:
        server.starttls()
        server.login(acc['email'], acc['app_password'])
        server.send_message(msg)
    print(f"✅ Email sent to {to} from {acc['email']}")

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'help'
    
    if cmd == 'unread':
        acc = sys.argv[2] if len(sys.argv) > 2 else 'info'
        check_unread(acc)
    elif cmd == 'list':
        acc = sys.argv[2] if len(sys.argv) > 2 else 'info'
        count = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        list_emails(acc, count)
    elif cmd == 'send':
        if len(sys.argv) < 5:
            print("Usage: gmail-monitor.py send <to> <subject> <body> [account]")
            sys.exit(1)
        acc = sys.argv[5] if len(sys.argv) > 5 else 'boris'
        send_email(sys.argv[2], sys.argv[3], sys.argv[4], acc)
    else:
        print("BORIS GMAIL MONITOR")
        print("Commands:")
        print("  unread [account]         - Check unread count")
        print("  list [account] [count]   - List latest emails")
        print("  send <to> <subj> <body>  - Send email as agent@yourdomain.com")
