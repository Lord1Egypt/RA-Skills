#!/usr/bin/env python3
"""
YouTube 频道订阅监控脚本 v2
每1小时检查新视频，提取字幕，生成摘要，推送到 Telegraph
"""

import os
import json
import subprocess
import re
from datetime import datetime
from pathlib import Path

# 配置
CHANNELS_FILE = "/home/t/.openclaw/workspace/youtube-channels.json"
STATE_FILE = "/home/t/.openclaw/workspace/youtube-state.json"
PROXY = {"http": "http://127.0.0.1:7897", "https": "http://127.0.0.1:7897"}
MAX_SUBTITLE_RETRIES = 3  # 最多检查3次
TELEGRAM_CHANNEL = "-1003899234137"

def send_telegram(message):
    """发送 Telegram 消息"""
    try:
        import requests
        token = "8630160870:AAFFF8xPS0muOqg8LGgMI3HalEA7ubVRIF8"
        
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = {
            "chat_id": TELEGRAM_CHANNEL,
            "text": message,
            "parse_mode": "Markdown"
        }
        resp = requests.post(url, json=data, timeout=10)
        return resp.status_code == 200
    except Exception as e:
        print(f"Telegram send error: {e}")
        return False

def load_channels():
    if os.path.exists(CHANNELS_FILE):
        with open(CHANNELS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f)

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {"last_check": {}, "processed_videos": {}, "pending_videos": {}}

def fetch_latest_videos(channel_url, limit=5):
    """获取频道最新视频"""
    cmd = [
        "yt-dlp", 
        "--flat-playlist",
        "--playlist-end", str(limit),
        "--print", "%(id)s|%(title)s|%(upload_date)s",
        channel_url
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120, env={**os.environ, "HTTP_PROXY": "http://127.0.0.1:7897", "HTTPS_PROXY": "http://127.0.0.1:7897"})
        if result.returncode != 0:
            print(f"Error fetching videos: {result.stderr}")
            return []
        
        videos = []
        for line in result.stdout.strip().split('\n'):
            if '|' in line:
                parts = line.split('|')
                if len(parts) >= 3:
                    videos.append({
                        'id': parts[0].strip(),
                        'title': parts[1].strip(),
                        'upload_date': parts[2].strip()
                    })
        return videos
    except Exception as e:
        print(f"Error: {e}")
        return []

def fetch_transcript(video_id, languages=["zh-Hans", "zh-Hant", "en"]):
    """获取视频字幕"""
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        import requests
        
        api = YouTubeTranscriptApi()
        transcript_list = api.list(video_id)
        
        # 尝试获取字幕
        for lang in languages:
            try:
                transcript = api.fetch(video_id, languages=[lang])
                texts = [s.text for s in transcript.snippets]
                return {
                    'text': '\n'.join(texts),
                    'language': transcript.language,
                    'language_code': lang
                }
            except:
                continue
        return None
    except Exception as e:
        print(f"Transcript error: {e}")
        return None

def translate_to_chinese(text):
    """用 Jina API 翻译成中文"""
    try:
        import requests
        url = "https://api.jina.ai/v1/translate"
        headers = {"Content-Type": "application/json"}
        data = {
            "source_lang": "en",
            "target_lang": "zh",
            "text": text[:5000]  # 限制长度
        }
        response = requests.post(url, json=data, headers=headers, timeout=30)
        if response.status_code == 200:
            return response.json().get("data", {}).get("translated_text", text)
    except Exception as e:
        print(f"Translation error: {e}")
    return text

def create_article(title, transcript_text, video_url, channel_name):
    """生成 Telegraph 文章"""
    # 简短摘要逻辑
    paragraphs = transcript_text.split('\n')
    summary = []
    total = 0
    for p in paragraphs[:15]:  # 取前15段
        if total + len(p) > 3000:
            break
        if p.strip():
            summary.append(p.strip())
            total += len(p)
    
    content_text = '\n'.join(summary)
    
    # 构建 Telegraph 格式
    content = [
        {"tag": "h3", "children": ["事件背景"]},
        {"tag": "p", "children": [content_text[:1500] + "..." if len(content_text) > 1500 else content_text]},
        {"tag": "hr"},
        {"tag": "p", "children": [f"来源：YouTube @ {channel_name}", " | ", f"查看完整视频：{video_url}"]}
    ]
    
    return content

def post_to_telegraph(title, content, author="虾总"):
    """发布到 Telegraph"""
    try:
        import requests
        import json
        
        # 先创建或获取 token
        account_data = {
            "short_name": "OpenClaw",
            "author_name": author
        }
        
        # 尝试获取已有 token
        token_file = "/home/t/.openclaw/workspace/telegraph_token.json"
        if os.path.exists(token_file):
            with open(token_file, 'r') as f:
                token_data = json.load(f)
                access_token = token_data.get("access_token")
        else:
            # 创建新账号
            resp = requests.post("https://api.telegra.ph/createAccount", json=account_data, timeout=10)
            if resp.status_code == 200:
                token_data = resp.json().get("result", {})
                access_token = token_data.get("access_token")
                with open(token_file, 'w') as f:
                    json.dump(token_data, f)
            else:
                return None
        
        if not access_token:
            return None
            
        # 创建页面
        page_data = {
            "access_token": access_token,
            "title": title[:256],
            "author_name": author,
            "content": json.dumps(content)
        }
        
        resp = requests.post("https://api.telegra.ph/createPage", json=page_data, timeout=30)
        if resp.status_code == 200:
            result = resp.json().get("result", {})
            return result.get("url")
    except Exception as e:
        print(f"Telegraph error: {e}")
    return None

def main():
    print(f"[{datetime.now()}] 开始检查 YouTube 频道...")
    
    channels = load_channels()
    if not channels:
        print("没有订阅的频道")
        return
    
    state = load_state()
    new_videos = []
    updated_videos = []  # 有字幕更新的视频
    
    for channel in channels:
        channel_url = channel.get('url')
        channel_name = channel.get('name', 'Unknown')
        print(f"检查频道: {channel_name}")
        
        videos = fetch_latest_videos(channel_url)
        
        for video in videos:
            video_id = video['id']
            
            # 初始化视频状态
            if video_id not in state['processed_videos']:
                state['processed_videos'][video_id] = {
                    'title': video['title'],
                    'channel': channel_name,
                    'channel_url': channel_url,
                    'check_count': 0,
                    'has_subtitle': False,
                    'posted': False
                }
                new_videos.append({**video, 'channel': channel_name, 'channel_url': channel_url})
            else:
                # 检查已存在的视频是否有字幕更新
                video_state = state['processed_videos'][video_id]
                if not video_state.get('has_subtitle') and not video_state.get('posted'):
                    # 之前没有字幕，现在再试一次
                    new_videos.append({**video, 'channel': channel_name, 'channel_url': channel_url})
    
    state['last_check'] = datetime.now().isoformat()
    
    if not new_videos:
        print("没有新视频需要处理")
        save_state(state)
        return
    
    print(f"发现 {len(new_videos)} 个视频需要处理")
    
    articles_to_send = []
    
    for video in new_videos:
        video_id = video['id']
        video_state = state['processed_videos'].get(video_id, {})
        check_count = video_state.get('check_count', 0) + 1
        
        print(f"处理视频: {video['title']} (检查第 {check_count} 次)")
        
        # 获取字幕
        transcript_data = fetch_transcript(video_id)
        
        if transcript_data:
            # 有字幕
            transcript_text = transcript_data['text']
            lang = transcript_data.get('language_code', 'zh')
            
            # 如果是英文，翻译成中文
            if lang == 'en':
                print("检测到英文字幕，翻译成中文...")
                transcript_text = translate_to_chinese(transcript_text)
            
            state['processed_videos'][video_id]['has_subtitle'] = True
            state['processed_videos'][video_id]['check_count'] = check_count
            
            # 生成文章
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            title = video['title'][:200]
            content = create_article(title, transcript_text, video_url, video['channel'])
            
            # 发布到 Telegraph
            url = post_to_telegraph(title, content)
            if url:
                articles_to_send.append({
                    'title': title,
                    'url': url,
                    'channel': video['channel']
                })
                state['processed_videos'][video_id]['posted'] = True
                print(f"已发布: {url}")
        else:
            # 没有字幕
            state['processed_videos'][video_id]['check_count'] = check_count
            
            if check_count >= MAX_SUBTITLE_RETRIES:
                print(f"视频 {video_id} 检查 {MAX_SUBTITLE_RETRIES} 次无字幕，跳过")
                state['processed_videos'][video_id]['posted'] = True  # 标记为已处理（跳过）
            else:
                print(f"暂无字幕，将在下一次检查 (第 {check_count + 1}/{MAX_SUBTITLE_RETRIES} 次)")
        
        # 保存状态
        save_state(state)
    
    # 输出需要发送的内容（供 OpenClaw 发送）
    if articles_to_send:
        print("---CONTENT_START---")
        for article in articles_to_send:
            msg = f"📺 *{article['title']}*\n{article['url']}"
            print(msg)
            # 发送 Telegram 消息
            send_telegram(msg)
        print("---CONTENT_END---")
    else:
        print("没有新文章需要发送")

if __name__ == "__main__":
    main()
