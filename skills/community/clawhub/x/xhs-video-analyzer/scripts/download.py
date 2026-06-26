#!/usr/bin/env python3
"""小红书视频下载器"""

import requests
import re
import json
import sys
import os

def download_xhs_video(url, output_dir="."):
    """下载小红书视频"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Referer': 'https://www.xiaohongshu.com/',
    }
    
    # 提取 note ID
    note_id_match = re.search(r'xiaohongshu\.com/explore/([a-f0-9]+)', url)
    if not note_id_match:
        note_id_match = re.search(r'xiaohongshu\.com/discovery/item/([a-f0-9]+)', url)
    
    note_id = note_id_match.group(1) if note_id_match else None
    
    try:
        # 方法1: 使用 API
        if note_id:
            api_url = f"https://www.xiaohongshu.com/discovery/item/{note_id}"
            resp = requests.get(api_url, headers=headers, timeout=30)
        else:
            resp = requests.get(url, headers=headers, timeout=30)
        
        # 从页面提取视频信息
        match = re.search(r'__INITIAL_STATE__\s*=\s*({.*?})\s*</script>', resp.text, re.DOTALL)
        
        if match:
            data = json.loads(match.group(1))
            note = data.get('note', {})
            video = note.get('video', {})
            media = video.get('media', {})
            stream = media.get('stream', {})
            
            # 尝试多种视频格式
            video_url = None
            for key in ['h264', 'h265', 'av1']:
                if stream.get(key):
                    h = stream[key][0] if isinstance(stream[key], list) else stream[key]
                    video_url = h.get('masterUrl')
                    if video_url:
                        break
            
            if video_url:
                print(f"📥 找到视频链接...")
                v_resp = requests.get(video_url, headers=headers, timeout=120)
                output_path = os.path.join(output_dir, 'video.mp4')
                with open(output_path, 'wb') as f:
                    f.write(v_resp.content)
                print(f"✅ 视频已保存: {output_path}")
                
                # 返回视频信息
                title = note.get('title', '未知标题')
                desc = note.get('desc', '')
                print(f"\n📋 标题: {title}")
                if desc:
                    print(f"📝 描述: {desc[:100]}...")
                
                return output_path
        
        print("❌ 未找到视频链接")
        return None
        
    except Exception as e:
        print(f"❌ 下载失败: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python download.py <xhs_url> [output_dir]")
        sys.exit(1)
    
    url = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "."
    download_xhs_video(url, output_dir)
