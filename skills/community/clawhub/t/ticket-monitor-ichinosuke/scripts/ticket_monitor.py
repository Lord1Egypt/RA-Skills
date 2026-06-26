import os
import json
import requests
import re
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# dotenv を使ってスクリプト実行ディレクトリ周辺の .env も読み込む
env_path = os.path.join(os.path.dirname(__file__), '../.env')
load_dotenv(dotenv_path=env_path)

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
# 春風亭一之輔 公式サイト
TARGET_URL = "https://www.ichinosuke-en.com/"
SEEN_TICKETS_FILE = os.path.join(os.path.dirname(__file__), "../data/seen_tickets.json")

def load_seen_tickets():
    if os.path.exists(SEEN_TICKETS_FILE):
        with open(SEEN_TICKETS_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_seen_tickets(seen_tickets):
    os.makedirs(os.path.dirname(SEEN_TICKETS_FILE), exist_ok=True)
    with open(SEEN_TICKETS_FILE, "w", encoding="utf-8") as f:
        json.dump(seen_tickets, f, ensure_ascii=False, indent=4)

def fetch_ticket_info():
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    response = requests.get(TARGET_URL, headers=headers)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, "html.parser")
    tickets = []
    
    # 日付から始まるリンクを探す (例: 03月10日(火)七代目...)
    date_pattern = re.compile(r"^\d{2}月\d{2}日")
    
    for a in soup.find_all("a", href=True):
        text = a.get_text(strip=True)
        if date_pattern.match(text):
            # テキストを分解して情報を抽出
            # 例: 03月10日(火)七代目 三遊亭円楽 芸歴２５周年記念落語会【開演】18:30【会場】有楽町よみうりホール
            
            # 会場を抽出
            venue_match = re.search(r"【会場】(.*)", text)
            venue = venue_match.group(1) if venue_match else "不明"
            
            # 東京の公演に限定する場合のフィルタリング（オプション）
            # ユーザーの要望「東京公演チケット」に対応
            is_tokyo = any(kw in venue or kw in text for kw in ["東京", "有楽町", "新宿", "高円寺", "大手町", "上野", "日本橋", "浅草"])
            
            if not is_tokyo:
                continue

            link = a["href"]
            if not link.startswith("http"):
                link = TARGET_URL + link.lstrip("/")
            
            # 公演名（日付と会場情報を除いた部分）を簡易的に抽出
            title = text
            if venue_match:
                title = text[:venue_match.start()].strip()
            
            # ユニークIDとしてリンクまたはテキストを使用
            ticket_id = link if "ticketInformation" in link else text
            
            tickets.append({
                "id": ticket_id,
                "title": title,
                "venue": venue,
                "url": link,
                "full_text": text
            })
            
    return tickets

def notify_discord(ticket):
    if not DISCORD_WEBHOOK_URL:
        print("DISCORD_WEBHOOK_URL is not set.")
        return

    data = {
        "content": f"🔔 **春風亭一之輔 公演情報(東京)**\n\n{ticket['full_text']}\n\n**詳細・チケット:** {ticket['url']}"
    }
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)
    response.raise_for_status()

def main():
    print("Checking for new tickets on official site...")
    try:
        current_tickets = fetch_ticket_info()
        seen_tickets = load_seen_tickets()
        
        new_tickets_found = False
        for ticket in current_tickets:
            if ticket["id"] not in seen_tickets:
                print(f"New ticket found: {ticket['title']}")
                notify_discord(ticket)
                seen_tickets.append(ticket["id"])
                new_tickets_found = True
        
        if new_tickets_found:
            save_seen_tickets(seen_tickets)
            print(f"Update completed. {len(current_tickets)} tickets tracked.")
        else:
            print("No new tickets found (all existing info already seen).")
            
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    main()
