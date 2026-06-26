#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YouTube 知識蒸餾器 v2
將 YouTube/Bilibili 影片轉化為結構化知識文章

使用方法：
    python youtube_distiller.py "URL" --style investment
    
觸發方式（蘇茉）：
    蘇茉，執行知識蒸餾 https://youtu.be/xxx --style investment
"""

import os
import sys
import argparse
import subprocess
import requests
import re
import datetime
from pathlib import Path

# 設定編碼
sys.stdout.reconfigure(encoding='utf-8')
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer)

# 設定
OUTPUT_DIR = r"C:\butler_sumo\temp\youtube-distiller"
YT_DLP_PATH = r"C:\butler_sumo\tools\youtube-knowledge\yt-dlp.exe"

# API 設定（從環境變數讀取）
API_KEY = os.getenv("MINIMAX_API_KEY", "")
API_URL = "https://api.minimax.io/v1/text/chatcompletion_v2"

# 支援的風格
STYLES = {
    "standard": "標準摘要",
    "academic": "學術筆記格式",
    "actions": "行動清單",
    "news": "新聞快訊格式",
    "investment": "投資分析格式",
    "podcast": "播客訪談格式",
    "eli5": "通俗易懂解釋",
    "bullets": "極簡子彈格式"
}

# 風格提示詞
STYLE_PROMPTS = {
    "standard": "請用簡潔的語言總結這個影片的主要內容。",
    "academic": "請用學術筆記的格式整理這個影片的內容，包括：標題、重點術語、關鍵概念、結論。",
    "actions": "請從這個影片中萃取出可行動的項目，列出具體的步驟或建議。",
    "news": "請用新聞快訊的格式撰寫這段內容的摘要，包括：時間、地點、人物、事件、要點。",
    "investment": """請用投資分析的格式整理這個影片內容，包括：
1. 市場趨勢和方向
2. 關鍵技術分析（支撐/壓力位、均線等）
3. 重要數據和指標
4. 板塊輪動和機會
5. 風險提示
6. 操作策略建議""",
    "podcast": "請用播客訪談的格式整理這個影片，保留對話的節奏感和個人觀點。",
    "eli5": "請用簡單易懂的語言解釋這個影片的內容，就像在跟一個不懂這個主題的人說明。",
    "bullets": "請用極簡的子彈格式列出這個影片的重點，每點不超過10個字。"
}

def log(msg):
    import datetime as dt
    print(f"[{dt.datetime.now().strftime('%H:%M:%S')}] {msg}")

def download_subtitles(url, output_path):
    """下載影片字幕"""
    log(f"正在下載字幕...")
    
    # 確保輸出目錄存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # 使用 yt-dlp 下載字幕
    cmd = [
        YT_DLP_PATH,
        "--write-subs",
        "--write-auto-subs",
        "--sub-lang", "zh,en,zh-Hans,zh-Hant",
        "--skip-download",
        "--output", output_path,
        url
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            log("字幕下載成功")
            return True
        else:
            log(f"字幕下載失敗: {result.stderr}")
            return False
    except Exception as e:
        log(f"下載錯誤: {e}")
        return False

def extract_subtitle_text(vtt_file):
    """從 VTT 檔案提取文字"""
    try:
        with open(vtt_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 移除 VTT 標籤和時間標記
        lines = content.split('\n')
        text_lines = []
        for line in lines:
            # 跳過空行、標籤和時間
            if line.strip() and not line.startswith('WEBVTT') and not line.startswith('NOTE') and not re.match(r'\d{2}:\d{2}', line) and not '-->' in line:
                text_lines.append(line.strip())
        
        return ' '.join(text_lines)
    except Exception as e:
        log(f"提取文字失敗: {e}")
        return None

def get_video_info(url):
    """取得影片資訊"""
    log(f"正在取得影片資訊...")
    
    cmd = [YT_DLP_PATH, "--dump-json", "--no-download", url]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            import json
            info = json.loads(result.stdout)
            return {
                "title": info.get("title", "未知標題"),
                "duration": info.get("duration", 0),
                "uploader": info.get("uploader", "未知作者")
            }
    except Exception as e:
        log(f"取得資訊失敗: {e}")
    
    return {"title": "未知標題", "duration": 0, "uploader": "未知作者"}

def ai_summarize(text, style="standard", video_info=None):
    """使用 AI 總結內容"""
    if not API_KEY:
        log("警告：未設定 API_KEY，使用基本總結")
        return text[:2000]  # 簡單截斷
    
    log(f"正在使用 AI 總結（風格：{STYLES.get(style, 'standard')}）...")
    
    # 構建提示詞
    style_prompt = STYLE_PROMPTS.get(style, STYLE_PROMPTS["standard"])
    
    system_prompt = """你是一個專業的內容分析師，擅長從影片字幕或文章中萃取有價值的資訊。"""
    
    user_prompt = f"""{style_prompt}

請分析以下內容：

---
{text[:8000]}  # 限制長度
---

請用繁體中文回覆。"""
    
    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "MiniMax-Abab6.5s",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "max_tokens": 2000,
            "temperature": 0.7
        }
        
        response = requests.post(API_URL, headers=headers, json=data, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            log(f"API response keys: {list(result.keys())}")
            
            # 嘗試不同的回應格式
            if "choices" in result and len(result["choices"]) > 0:
                choice = result["choices"][0]
                if isinstance(choice, dict):
                    # 標準格式
                    if "message" in choice:
                        return choice["message"].get("content", text[:2000])
                    elif "text" in choice:
                        return choice["text"]
                # 如果 choices[0] 是 None 或格式不同
                log(f"Choices content: {choice}")
            
            # 嘗試其他可能的格式
            if "base_resp" in result:
                log(f"base_resp: {result['base_resp']}")
            
            log(f"API response: {result}")
            return text[:2000]
        else:
            log(f"API 錯誤: {response.status_code} - {response.text}")
            return text[:2000]
            
    except Exception as e:
        log(f"AI 總結失敗: {e}")
        return text[:2000]


def sync_to_sumonotebook(summary_file, video_title, video_url, category="research"):
    """同步摘要到 SumoNoteBook"""
    sumo_raw = Path("C:/butler_sumo/library/SumoNoteBook/raw/shared")
    
    # 以 YYYYMMDD__Main__標題.md 格式命名
    date_str = datetime.datetime.now().strftime("%Y%m%d")
    time_str = datetime.datetime.now().strftime("%H:%M")
    safe_title = "".join(c for c in video_title[:30] if c.isalnum() or c in ' -_')
    filename = f"{date_str}__Main__{safe_title}.md"
    
    # 確保目錄存在
    sumo_raw.mkdir(parents=True, exist_ok=True)
    
    dest = sumo_raw / filename
    
    # 讀取摘要內容
    with open(summary_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 寫入 SumoNoteBook
    with open(dest, 'w', encoding='utf-8') as f:
        f.write(content)
    
    log(f"已同步到 SumoNoteBook：{dest}")
    
    # 更新 sync_log.md
    update_sync_log(video_title, video_url, category, time_str)
    
    # 更新 research_index.md
    update_research_index(video_title, video_url, category, time_str)
    
    return dest


def update_sync_log(video_title, video_url, category, time_str):
    """更新同步日誌"""
    sync_log_path = Path("C:/butler_sumo/tools/youtube-distiller/sync_log.md")
    
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    new_entry = f"""## [{timestamp}] SYNC | {video_title}
- 分類: {category}
- URL: {video_url}
- 狀態: 完成
"""
    
    # 檢查檔案是否存在
    if sync_log_path.exists():
        with open(sync_log_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 檢查是否已經有今天的條目
        if date_str not in content:
            new_entry = "# YouTube Distiller 同步日誌\n\n" + new_entry
            content = new_entry + "\n\n" + content
        else:
            content = content.replace("# YouTube Distiller 同步日誌\n\n", "# YouTube Distiller 同步日誌\n\n" + new_entry + "\n", 1)
    else:
        new_entry = "# YouTube Distiller 同步日誌\n\n" + new_entry
    
    with open(sync_log_path, 'w', encoding='utf-8') as f:
        f.write(content)


def update_research_index(video_title, video_url, category, time_str):
    """更新研究索引"""
    index_path = Path("C:/butler_sumo/library/SumoNoteBook/Sumo_wiki/research_index.md")
    
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    new_entry = f"- [{time_str}] {video_title} - [YouTube]({video_url}) - ✅ 完成"
    
    # 確保目錄存在
    index_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 檢查檔案是否存在
    if index_path.exists():
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 檢查是否有當天日期區塊
        if f"### {date_str}" in content:
            # 附加到當天
            content = content.replace(
                f"### {date_str}\n",
                f"### {date_str}\n{new_entry}\n"
            )
        else:
            # 新增當天區塊
            new_section = f"""
### {date_str}
{new_entry}
"""
            if "## 按日期" in content:
                content = content.replace("## 按日期", "## 按日期" + new_section)
            else:
                content = "# 📚 研究索引\n\n> 追蹤所有研究記錄\n\n## 按日期" + new_section + "\n" + content
    else:
        # 建立新檔案
        content = f"""# 📚 研究索引

> 追蹤所有研究記錄

## 按日期

### {date_str}
{new_entry}

## 按分類

### Agent 技術
- （待分類）

### Prompt 設計
- （待分類）

### 研究報告
- （待分類）
"""
    
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    log(f"已更新研究索引：{index_path}")

def main():
    parser = argparse.ArgumentParser(description="YouTube 知識蒸餾器")
    parser.add_argument("url", help="YouTube 或 Bilibili 影片 URL")
    parser.add_argument("--style", "-s", default="standard", 
                        choices=list(STYLES.keys()),
                        help=f"摘要風格：{', '.join(STYLES.keys())}")
    parser.add_argument("--output", "-o", help="輸出檔案路徑")
    parser.add_argument("--no-whisper", action="store_true", help="只使用字幕，不使用 Whisper")
    parser.add_argument("--model", "-m", default="tiny", help="Whisper 模型大小")
    parser.add_argument("--no-sync", action="store_true", help="不同步到 SumoNoteBook")
    
    args = parser.parse_args()
    
    log("=" * 50)
    log("YouTube 知識蒸餾器 v2")
    log("=" * 50)
    
    # 取得影片資訊
    video_info = get_video_info(args.url)
    log(f"標題：{video_info['title']}")
    log(f"作者：{video_info['uploader']}")
    log(f"時長：{video_info['duration']} 秒")
    log(f"風格：{STYLES[args.style]}")
    
    # 確保輸出目錄存在
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 下載字幕
    base_path = os.path.join(OUTPUT_DIR, "temp_video")
    subtitle_path = download_subtitles(args.url, base_path)
    
    # 嘗試讀取字幕
    text = None
    vtt_files = [
        base_path + ".zh.vtt",
        base_path + ".en.vtt",
        base_path + ".zh-Hans.vtt",
        base_path + ".zh-Hant.vtt",
        base_path + ".vtt"
    ]
    
    for vtt_file in vtt_files:
        if os.path.exists(vtt_file):
            text = extract_subtitle_text(vtt_file)
            if text:
                log(f"成功讀取字幕：{vtt_file}")
                break
    
    if not text:
        log("無法取得字幕，請手動提供文字內容")
        sys.exit(1)
    
    # AI 總結
    summary = ai_summarize(text, args.style, video_info)
    
    # 輸出結果
    output_file = args.output
    if not output_file:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(OUTPUT_DIR, f"summary_{timestamp}.txt")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"# {video_info['title']}\n")
        f.write(f"作者：{video_info['uploader']}\n")
        f.write(f"網址：{args.url}\n")
        f.write(f"風格：{STYLES[args.style]}\n")
        f.write(f"時間：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("\n" + "=" * 50 + "\n\n")
        f.write(summary)
    
    log(f"\n完成！摘要已儲存至：{output_file}")
    
    # 同步到 SumoNoteBook
    if not args.no_sync:
        sync_to_sumonotebook(output_file, video_info['title'], args.url)
    
    # 顯示摘要
    print("\n" + "=" * 50)
    print("摘要內容：")
    print("=" * 50)
    print(summary)

if __name__ == "__main__":
    main()
