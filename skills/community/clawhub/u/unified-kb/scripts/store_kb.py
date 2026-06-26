#!/home/xdl/antigravity_workspace/venv/bin/python3
"""
统一知识库入库脚本 (unified-kb)
触发条件：用户发送内容并标记 #kb
协同存储：IMA 知识库 + workspace KB + memory 记录

支持内容类型：
  wechat   - 微信公众号文章
  link     - 普通网页链接
  youtube  - YouTube 视频（字幕提取 + 总结生成）
  text     - 纯文本
  file     - 本地文件路径
"""

import sys
import os
import re
import json
import requests
import subprocess
import datetime
from pathlib import Path

# ========== 配置 ==========
WORKSPACE_KB = "/home/xdl/.openclaw/workspace/kb"
MEMORY_DIR = "/home/xdl/.openclaw/workspace/memory"
DATE_TODAY = datetime.datetime.now().strftime('%Y-%m-%d')
DATE_PREFIX = datetime.datetime.now().strftime('%Y%m%d')
YOUTUBE_COOKIES = "/tmp/youtube_cookies.txt"

# IMA 默认知识库：个人知识库
IMA_KB_ID = "3ABKKskfyVyAHq_ohwX7KrwDyfrapnxTTHlQ85NFR6E="


def load_ima_env():
    """加载 IMA 凭证"""
    IMA_CLIENT_ID = ""
    IMA_API_KEY = ""
    try:
        env_content = open("/home/xdl/.openclaw/workspace/.secrets/ima.env").read()
        for line in env_content.strip().split('\n'):
            line = line.strip()
            if not line or line.startswith('#'): continue
            if line.startswith("IMA_OPENAPI_CLIENTID"):
                IMA_CLIENT_ID = line.split("=", 1)[1].strip("'\" \t")
            elif line.startswith("IMA_OPENAPI_APIKEY"):
                IMA_API_KEY = line.split("=", 1)[1].strip("'\" \t")
    except:
        pass
    return IMA_CLIENT_ID, IMA_API_KEY


def ima_api(path, body):
    """调用 IMA OpenAPI"""
    IMA_CLIENT_ID, IMA_API_KEY = load_ima_env()
    if not IMA_CLIENT_ID or not IMA_API_KEY:
        return None, "IMA凭证未配置"
    try:
        resp = requests.post(
            f"https://ima.qq.com/{path}",
            headers={
                "ima-openapi-clientid": IMA_CLIENT_ID,
                "ima-openapi-apikey": IMA_API_KEY,
                "Content-Type": "application/json; charset=utf-8"
            },
            json=body,
            timeout=30
        )
        return resp.json(), None
    except Exception as e:
        return None, str(e)


def ensure_utf8(text):
    """确保字符串为合法UTF-8"""
    if isinstance(text, bytes):
        for enc in ['utf-8', 'gbk', 'gb2312', 'latin-1']:
            try:
                return text.decode(enc)
            except:
                continue
    return text


def download_wechat(url):
    """下载微信公众号文章"""
    script = "/home/xdl/.openclaw/workspace/skills/wechat-article-reader/scripts/export.py"
    output_dir = "/tmp/kb_wechat"
    os.makedirs(output_dir, exist_ok=True)
    try:
        result = subprocess.run(
            ["python3", script, url, output_dir],
            capture_output=True, text=True, timeout=30
        )
        output = result.stdout + result.stderr
        for line in output.split('\n'):
            if '已导出到:' in line:
                path = line.split('已导出到:')[1].strip()
                return path, None
            elif 'exported to:' in line:
                path = line.split('exported to:')[1].strip()
                return path, None
        return None, "未找到导出文件"
    except Exception as e:
        return None, f"下载失败: {e}"


def is_youtube_url(url):
    """判断是否为 YouTube 链接"""
    return bool(re.search(r'(youtu\.be|youtube\.com/(watch|embed|shorts))', url))


def is_x_url(url):
    """判断是否为 X/Twitter 链接"""
    return bool(re.search(r'(x\.com|twitter\.com)', url))


def fetch_youtube_info(url):
    """通过 oEmbed 获取 YouTube 视频基本信息"""
    try:
        match = re.search(r'(?:v=|/)([a-zA-Z0-9_-]{11})', url)
        if not match:
            return None, "无法解析YouTube视频ID"
        video_id = match.group(1)
        oembed_url = f"https://www.youtube.com/oembed?url=https://youtu.be/{video_id}&format=json"
        resp = requests.get(oembed_url, timeout=10)
        if resp.status_code != 200:
            return None, f"oEmbed请求失败: {resp.status_code}"
        data = resp.json()
        return {
            "title": data.get("title", "YouTube视频"),
            "author": data.get("author_name", ""),
            "video_id": video_id,
            "url": url
        }, None
    except Exception as e:
        return None, f"YouTube信息获取失败: {e}"


def download_youtube_subtitles(url):
    """
    下载 YouTube 视频字幕
    使用 TV client + node.js JS runtime + cookies 绕过机器人验证
    返回: (vtt_filepath, error)
    """
    # 检查 cookies 文件是否存在
    if not os.path.exists(YOUTUBE_COOKIES):
        return None, f"Cookies 文件不存在: {YOUTUBE_COOKIES}，请先配置 YouTube cookies"

    output_template = "/tmp/subs.%(ext)s"
    cmd = [
        'yt-dlp',
        '--js-runtimes', 'node:/usr/bin/node',
        '--cookies', YOUTUBE_COOKIES,
        '--extractor-args', 'youtube:player_client=tv',
        '--write-subs',
        '--skip-download',
        '-o', output_template,
        url
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode != 0:
            return None, f"yt-dlp 失败: {result.stderr[-500:]}"
        
        # 查找下载的字幕文件
        for ext in ['vtt', 'srt', 'ass']:
            vtt_path = f"/tmp/subs.{ext}"
            if os.path.exists(vtt_path):
                return vtt_path, None
        return None, "未找到字幕文件"
    except subprocess.TimeoutExpired:
        return None, "字幕下载超时（>120秒）"
    except Exception as e:
        return None, f"字幕下载异常: {e}"


def parse_vtt_to_text(vtt_path):
    """
    解析 VTT 字幕文件，提取纯文本
    返回: (full_text, num_segments)
    """
    try:
        with open(vtt_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return None, f"读取字幕文件失败: {e}"

    # 解析 VTT 格式
    # 格式: 00:00:08.975 --> 00:00:11.745\n文本内容\n\n
    segments = re.findall(
        r'(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})\s*\n(.+?)(?=\n\n|\n\d{2}:)',
        content, re.DOTALL
    )

    if not segments:
        # 尝试另一种格式（无空格的时间戳）
        segments = re.findall(
            r'(\d{2}:\d{2}:\d{2}\.\d{3})-->(\d{2}:\d{2}:\d{2}\.\d{3})\s*\n(.+?)(?=\n\n|\n\d{2}:)',
            content, re.DOTALL
        )

    full_text = '\n'.join([s[-1].strip().replace('\n', ' ') for s in segments if s[-1].strip()])
    return full_text, len(segments)


def generate_summary(full_text, video_info):
    """
    基于字幕文本生成总结
    简单实现：提取开头、结尾和中间关键段落
    """
    title = video_info.get('title', 'YouTube视频')
    video_id = video_info.get('video_id', '')
    url = video_info.get('url', '')
    author = video_info.get('author', '')

    # 取前 5000 字符作为样本生成总结
    sample = full_text[:5000]
    
    summary_lines = [
        f"# {title}",
        f"",
        f"**影片來源**: {url}",
        f"**頻道**: {author}",
        f"",
        f"**內容大綱**: （基于字幕内容生成）",
        f"",
    ]

    # 从字幕样本中提取核心主题（简化版：取前中后各一段）
    lines = sample.split('\n')
    if len(lines) > 3:
        # 前三行通常是开场
        summary_lines.append(f"**开场**: {' '.join(lines[:3])}")
    
    # 中间部分
    mid = len(lines) // 2
    if len(lines) > mid + 3:
        summary_lines.append(f"**中段**: {' '.join(lines[mid:mid+3])}")

    # 检查视频长度，推测主题
    text_sample = sample.replace('\n', '')[:1000]
    
    summary = f"""# {title}

**影片來源**: {url}
**頻道**: {author}

---

## 內容摘要

{text_sample[:2000]}...

---

*字幕共 {len(full_text)} 字，内容详见完整字幕文件*
"""
    return summary


def fetch_x_info(url):
    """通过网页抓取获取 X/Twitter 内容摘要"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
        }
        resp = requests.get(url, timeout=15, headers=headers, allow_redirects=True)
        resp.encoding = resp.apparent_encoding or 'utf-8'
        title_match = re.search(r'<title[^>]*>(.*?)</title>', resp.text, re.S)
        title = title_match.group(1).strip().replace(' | X', '').replace(' / X', '') if title_match else "X推文"
        content = re.sub(r'<[^>]+>', '', resp.text)[:2000]
        return {"title": title, "content": content, "url": url}, None
    except Exception as e:
        return None, f"X内容获取失败: {e}"


def fetch_webpage(url):
    """抓取普通网页"""
    try:
        resp = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
        resp.encoding = resp.apparent_encoding or 'utf-8'
        title = re.search(r'<title[^>]*>(.*?)</title>', resp.text, re.S)
        title = title.group(1).strip() if title else url
        content = re.sub(r'<[^>]+>', '', resp.text)[:3000]
        return {"title": title, "content": content, "url": url}, None
    except Exception as e:
        return None, f"抓取失败: {e}"


def get_root_folder_id(kb_id):
    """获取知识库的根目录 folder_id"""
    result, err = ima_api("openapi/wiki/v1/get_knowledge_list", {
        "cursor": "", "limit": 1, "knowledge_base_id": kb_id
    })
    if err or not result or result.get("code") != 0:
        return None
    data = result.get("data", {})
    items = data.get("knowledge_list", [])
    if items:
        return items[0].get("parent_folder_id")
    return None


def save_to_ima_urls(urls, kb_id):
    """使用 import_urls 存入 IMA 知识库"""
    folder_id = get_root_folder_id(kb_id)
    if not folder_id:
        return False, "无法获取知识库folder_id"
    body = {
        "urls": urls if isinstance(urls, list) else [urls],
        "knowledge_base_id": kb_id,
        "folder_id": folder_id
    }
    result, err = ima_api("openapi/wiki/v1/import_urls", body)
    if err:
        return False, err
    if result and result.get("code") == 0:
        return True, "IMA知识库存储成功"
    return False, f"IMA返回: {result}"


def save_to_ima_notes(title, content, tags, append_to_doc_id=None):
    """
    存入 IMA 笔记
    如果 append_to_doc_id 提供，则追加到已有笔记
    否则创建新笔记
    """
    if append_to_doc_id:
        # 追加到已有笔记
        body = {
            "doc_id": append_to_doc_id,
            "content_format": 1,
            "content": "\n\n" + content
        }
        path = "openapi/note/v1/append_doc"
    else:
        # 新建笔记
        body = {
            "content_format": 1,
            "content": content,
            "title": title[:200] if title else "无标题"
        }
        path = "openapi/note/v1/import_doc"

    result, err = ima_api(path, body)
    if err:
        return None, err
    if result and result.get("code") == 0:
        note_id = result.get("data", {}).get("note_id") or append_to_doc_id
        return note_id, "成功"
    return None, f"IMA返回: {result}"


def save_to_ima_notes_chunked(title, content, tags):
    """
    分段存入 IMA 笔记（内容过长时）
    每段 ~12000 字符，先 import_doc 再多次 append_doc
    """
    chunk_size = 12000
    chunks = [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]
    
    print(f"  内容 {len(content)} 字，分 {len(chunks)} 段上传...")
    
    # 第一段：import_doc
    first_chunk = f"# {title}\n\n{chunks[0]}"
    note_id, err = save_to_ima_notes(title, first_chunk, tags)
    if err != None and "成功" not in str(err):
        return None, err
    
    # 后续段：append_doc
    for i in range(1, len(chunks)):
        note_id, err = save_to_ima_notes(title, chunks[i], tags, append_to_doc_id=note_id)
        if err is not None and "成功" not in str(err):
            return note_id, f"第{i+1}段追加失败: {err}"
    
    return note_id, "成功"


def save_to_workspace_kb(title, content, source, tags, suffix=""):
    """存入 workspace/kb 目录"""
    os.makedirs(WORKSPACE_KB, exist_ok=True)
    safe_title = re.sub(r'[\\/:*?"<>|]', '', title)[:50]
    if suffix:
        suffix = f"_{suffix}"
    filename = f"{DATE_PREFIX}_{safe_title}{suffix}.md"
    filepath = os.path.join(WORKSPACE_KB, filename)

    tag_line = " ".join([f"#{t.strip('#')}" for t in tags]) if tags else "#kb"
    full_content = f"""---
title: {title}
source: {source}
date: {DATE_TODAY}
tags: {tag_line}
---

# {title}

{content}
"""

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(full_content)
        return True, filepath
    except Exception as e:
        return False, f"KB写入失败: {e}"


def save_text_file(title, content, suffix=""):
    """存入 workspace/kb 目录（纯文本文件，无 Markdown 格式）"""
    os.makedirs(WORKSPACE_KB, exist_ok=True)
    safe_title = re.sub(r'[\\/:*?"<>|]', '', title)[:50]
    if suffix:
        suffix = f"_{suffix}"
    filename = f"{DATE_PREFIX}_{safe_title}{suffix}.txt"
    filepath = os.path.join(WORKSPACE_KB, filename)

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, filepath
    except Exception as e:
        return False, f"文本文件写入失败: {e}"


def record_to_memory(title, source, kb_paths, tags, ima_note_id, ima_kb_status):
    """记录到 memory/YYYY-MM-DD.md"""
    os.makedirs(MEMORY_DIR, exist_ok=True)
    memory_file = os.path.join(MEMORY_DIR, f"{DATE_TODAY}.md")
    tag_str = " ".join([f"#{t.strip('#')}" for t in tags]) if tags else "#kb"
    
    kb_paths_str = " | ".join([f"`{p}`" for p in kb_paths if p]) if kb_paths else ""
    line = f"- **KB入库**：{title} | 来源：{source} | 路径：{kb_paths_str} | IMA笔记：{ima_note_id} | IMA知识库：{ima_kb_status} | 标签：{tag_str}\n"
    
    try:
        with open(memory_file, 'a', encoding='utf-8') as f:
            f.write(line)
        return True
    except:
        return False


def process_youtube_video(url, tags):
    """
    处理 YouTube 视频：下载字幕 → 生成总结 → 存入 IMA + KB
    返回: (note_ids, kb_paths, error)
    """
    print(f"\n📥 开始处理 YouTube 视频: {url}")
    
    # Step 1: 获取视频基本信息
    print("  ① 获取视频信息...")
    video_info, err = fetch_youtube_info(url)
    if err:
        return None, None, f"获取视频信息失败: {err}"
    print(f"  ✓ 标题: {video_info['title']}")
    print(f"  ✓ 频道: {video_info['author']}")
    
    # Step 2: 下载字幕
    print("  ② 下载字幕...")
    vtt_path, err = download_youtube_subtitles(url)
    if err:
        return None, None, f"字幕下载失败: {err}"
    print(f"  ✓ 字幕文件: {vtt_path}")
    
    # Step 3: 解析字幕
    print("  ③ 解析字幕...")
    full_text, num_segments = parse_vtt_to_text(vtt_path)
    if not full_text:
        return None, None, f"字幕解析失败: {num_segments}"
    print(f"  ✓ 字幕 {num_segments} 条，共 {len(full_text)} 字")
    
    # Step 4: 生成总结
    print("  ④ 生成总结...")
    summary = generate_summary(full_text, video_info)
    print(f"  ✓ 总结生成完成")
    
    # Step 5: 存入 IMA 笔记（分段）
    print("  ⑤ 存入 IMA 笔记...")
    note_id, err = save_to_ima_notes_chunked(
        video_info['title'] + " 字幕原文",
        full_text,
        tags
    )
    if err and "成功" not in str(err):
        print(f"  ⚠️ IMA 笔记失败: {err}")
        note_id = None
    else:
        print(f"  ✓ IMA 笔记: {note_id}")
    
    # 同时存一份总结笔记
    summary_note_id, _ = save_to_ima_notes(
        video_info['title'] + " 总结",
        summary,
        tags
    )
    print(f"  ✓ 总结笔记: {summary_note_id}")
    
    # Step 6: 存入 IMA 知识库（视频链接作为来源引用）
    print("  ⑥ 存入 IMA 知识库...")
    ima_kb_ok, ima_kb_msg = save_to_ima_urls(url, IMA_KB_ID)
    print(f"  {'✓' if ima_kb_ok else '⚠️'} IMA知识库: {ima_kb_msg}")
    
    # Step 7: 存入 workspace/kb
    print("  ⑦ 存入 workspace/kb...")
    kb_paths = []
    
    _, summary_path = save_to_workspace_kb(
        video_info['title'] + "_总结",
        summary,
        url,
        tags
    )
    if summary_path:
        kb_paths.append(summary_path)
        print(f"  ✓ 总结: {summary_path}")
    
    _, subs_path = save_text_file(
        video_info['title'] + "_字幕原文",
        full_text,
        "字幕原文"
    )
    if subs_path:
        kb_paths.append(subs_path)
        print(f"  ✓ 字幕: {subs_path}")
    
    # Step 8: 记录 memory
    print("  ⑧ 记录 memory...")
    note_ids = f"总结:{summary_note_id} 字幕:{note_id}"
    mem_ok = record_to_memory(
        video_info['title'],
        url,
        kb_paths,
        tags,
        note_ids,
        "✅" if ima_kb_ok else "❌"
    )
    print(f"  {'✓' if mem_ok else '⚠️'} Memory记录")
    
    all_note_ids = [n for n in [summary_note_id, note_id] if n]
    return all_note_ids, kb_paths, None


def main():
    if len(sys.argv) < 3:
        print("❌ 参数不足: content_type content [tags]")
        print("  content_type: wechat | link | youtube | text | file")
        print("  示例: python3 store_kb.py youtube 'https://youtu.be/xxx' #半导体")
        sys.exit(1)

    content_type = sys.argv[1]
    content = sys.argv[2]
    tags = sys.argv[3:] if len(sys.argv) > 3 else []

    result_msg = []
    title = ""
    source_url = ""
    kb_paths = []
    note_ids = []
    ima_kb_status = "❌"

    # ========== 各类内容处理 ==========
    
    if content_type == "youtube":
        # YouTube 视频：完整字幕提取流程
        note_ids, kb_paths, err = process_youtube_video(content, tags)
        if err:
            print(f"❌ {err}")
            sys.exit(1)
        title = "YouTube视频字幕提取"
        source_url = content
        note_ids_str = ", ".join([str(n) for n in note_ids]) if note_ids else "失败"
        result_msg.append(f"IMA笔记: ✅ {note_ids_str}")
        result_msg.append(f"本地KB: ✅ {len(kb_paths)} 个文件")
        ima_kb_status = "✅"

    elif content_type == "wechat":
        # 微信公众号
        path, err = download_wechat(content)
        if err:
            print(f"❌ {err}")
            sys.exit(1)
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
        m = re.search(r'^#\s+(.+)$', text, re.M)
        title = m.group(1).strip() if m else "微信文章"
        source_url = content
        
        # 存 IMA 知识库
        ima_kb_ok, ima_kb_msg = save_to_ima_urls(content, IMA_KB_ID)
        result_msg.append(f"IMA知识库: {'✅' if ima_kb_ok else '❌ ' + ima_kb_msg}")
        ima_kb_status = "✅" if ima_kb_ok else "❌"

        # 存 IMA 笔记（完整正文）
        note_id, _ = save_to_ima_notes(title, text, tags)
        if note_id:
            note_ids.append(note_id)
        result_msg.append(f"IMA笔记: ✅ {note_id}")

        # 存 workspace/kb
        kb_ok, kb_result = save_to_workspace_kb(title, text, source_url, tags)
        result_msg.append(f"本地KB: {'✅ ' + kb_result if kb_ok else '❌ ' + kb_result}")
        if kb_ok:
            kb_paths.append(kb_result)

    elif content_type == "link":
        if is_youtube_url(content):
            # YouTube 链接（非 #kb 模式，只获取基本信息）
            data, err = fetch_youtube_info(content)
            if err:
                print(f"❌ {err}")
                sys.exit(1)
            title = data["title"]
            source_url = content
            note_body = f"标题：{title}\n作者：{data['author']}\n链接：{content}\n\n这是一条YouTube视频摘要记录。"
            
            note_id, _ = save_to_ima_notes(title, note_body, tags)
            if note_id:
                note_ids.append(note_id)
            result_msg.append(f"IMA笔记: ✅ {note_id}")
            
        elif is_x_url(content):
            data, err = fetch_x_info(content)
            if err:
                print(f"❌ {err}")
                sys.exit(1)
            title = data["title"]
            source_url = content
            
            note_id, _ = save_to_ima_notes(title, data["content"], tags)
            if note_id:
                note_ids.append(note_id)
            result_msg.append(f"IMA笔记: ✅ {note_id}")
            
        else:
            # 普通网页
            data, err = fetch_webpage(content)
            if err:
                print(f"❌ {err}")
                sys.exit(1)
            title = data["title"]
            source_url = content
            
            ima_kb_ok, ima_kb_msg = save_to_ima_urls(content, IMA_KB_ID)
            result_msg.append(f"IMA知识库: {'✅' if ima_kb_ok else '❌ ' + ima_kb_msg}")
            ima_kb_status = "✅" if ima_kb_ok else "❌"

            # 存 IMA 笔记（完整正文）
            note_id, _ = save_to_ima_notes(title, data["content"], tags)
            if note_id:
                note_ids.append(note_id)
            result_msg.append(f"IMA笔记: ✅ {note_id}")

            kb_ok, kb_result = save_to_workspace_kb(title, data["content"], source_url, tags)
            result_msg.append(f"本地KB: {'✅ ' + kb_result if kb_ok else '❌ ' + kb_result}")
            if kb_ok:
                kb_paths.append(kb_result)

    elif content_type == "text":
        title = content[:50] + ("..." if len(content) > 50 else "")
        source_url = ""
        note_id, _ = save_to_ima_notes(title, content, tags)
        if note_id:
            note_ids.append(note_id)
        result_msg.append(f"IMA笔记: ✅ {note_id}")
        
        kb_ok, kb_result = save_to_workspace_kb(title, content, "纯文本", tags)
        result_msg.append(f"本地KB: {'✅ ' + kb_result if kb_ok else '❌ ' + kb_result}")
        if kb_ok:
            kb_paths.append(kb_result)

    elif content_type == "file":
        filepath = content
        ext = os.path.splitext(filepath)[1].lower()
        title = os.path.basename(filepath)
        source_url = ""
        text = None

        # MarkItDown 支持的二进制格式：优先用转换器
        md_convertible = {'.pdf', '.docx', '.doc', '.pptx', '.ppt',
                          '.xlsx', '.xls', '.jpg', '.jpeg', '.png',
                          '.gif', '.bmp', '.mp3', '.wav', '.html'}

        # 文本格式：直接读取
        text_readable = {'.txt', '.md', '.csv', '.json', '.xml', '.html', '.htm',
                         '.py', '.js', '.sh', '.yaml', '.yml', '.toml'}

        try:
            if ext in md_convertible:
                # 用 MarkItDown 转换二进制/多媒体文件
                try:
                    from markitdown import MarkItDown
                    md = MarkItDown()
                    with open(filepath, 'rb') as f:
                        result = md.convert_stream(f, file_extension=ext.lstrip('.'))
                    text = result.text_content
                    print(f"  MarkItDown 转换成功 ({ext} → {len(text)} 字)")
                except ImportError:
                    print(f"  ⚠️ MarkItDown 未安装，跳过转换，尝试纯文本读取")
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        text = f.read()
                except Exception as e:
                    print(f"  ⚠️ MarkItDown 转换失败: {e}，回退到纯文本读取")
                    try:
                        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                            text = f.read()
                    except Exception:
                        text = None

            elif ext in text_readable:
                # 文本文件：直接读取
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    text = f.read()
            else:
                # 未知格式：尝试 MarkItDown 再回退到文本
                try:
                    from markitdown import MarkItDown
                    md = MarkItDown()
                    with open(filepath, 'rb') as f:
                        result = md.convert_stream(f, file_extension=ext.lstrip('.'))
                    text = result.text_content
                    print(f"  MarkItDown 转换成功 ({ext} → {len(text)} 字)")
                except Exception:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        text = f.read()

            if text is None:
                print(f"❌ 无法提取文件内容: {filepath}")
                sys.exit(1)

            note_id, _ = save_to_ima_notes(title, text, tags)
            if note_id:
                note_ids.append(note_id)
            result_msg.append(f"IMA笔记: ✅ {note_id}")

            kb_ok, kb_result = save_to_workspace_kb(title, text, "本地文件", tags)
            result_msg.append(f"本地KB: {'✅ ' + kb_result if kb_ok else '❌ ' + kb_result}")
            if kb_ok:
                kb_paths.append(kb_result)

        except Exception as e:
            print(f"❌ 读取文件失败: {e}")
            sys.exit(1)

    else:
        print(f"❌ 未知 content_type: {content_type}")
        sys.exit(1)

    # Memory 记录（对于 youtube 类型已在上方处理）
    if content_type != "youtube":
        note_ids_str = ", ".join([str(n) for n in note_ids]) if note_ids else "无"
        mem_ok = record_to_memory(title, source_url, kb_paths, tags, note_ids_str, ima_kb_status)
        result_msg.append(f"Memory记录: {'✅' if mem_ok else '❌'}")

    # 重建 KB 索引（自动同步 kb_master_index.md）
    try:
        import subprocess
        rebuild_script = "/home/xdl/.openclaw/workspace/scripts/rebuild_kb_index.py"
        result = subprocess.run(["python3", rebuild_script], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            result_msg.append("KB索引: ✅ 已更新")
        else:
            result_msg.append(f"KB索引: ⚠️ 更新失败")
    except Exception as e:
        result_msg.append(f"KB索引: ⚠️ 跳过 ({str(e)[:30]})")

    # 输出结果
    print("\n" + "\n".join(result_msg))
    print(f"\n📚 标题: {title}")


if __name__ == "__main__":
    main()
