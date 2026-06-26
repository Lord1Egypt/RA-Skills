#!/usr/bin/env python3
"""
WeChat Article Scraper & Feishu Importer v2.1
从微信公众号抓取文章（图片+文字），按原顺序导入飞书知识库。

改进 v2.1：
- 解析时直接下载图片（不单独走一遍）
- 生成含本地路径的完整 Markdown
- 输出 Markdown 内容供直接写入飞书

流程：
1. 用 Chrome headless 抓取完整 HTML（绕过反爬）
2. 解析 HTML，提取所有内容块（文字/图片/GIF视频）
   - 解析时同步下载图片到本地
   - 输出含本地图片路径的完整 Markdown
3. 创建飞书文档 → 用 Markdown 写入 → 插入所有图片（末尾追加）
4. 用户手动调整图片位置
"""

import sys
import json
import re
import os
import subprocess
import urllib.request
import urllib.parse
import tempfile
import time
import argparse
import datetime


# ============================================================
# 1. 浏览器抓取
# ============================================================

CHROME_PATH = "/usr/bin/google-chrome"

ANTI_DETECT_ARGS = [
    "--headless=new",
    "--disable-gpu",
    "--no-sandbox",
    "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "--disable-blink-features=AutomationControlled",
    "--no-first-run",
    "--no-default-browser-check",
]

def fetch_article_html(url: str, timeout: int = 40) -> str:
    """用 Chrome headless 抓取文章完整 HTML"""
    cmd = [CHROME_PATH] + ANTI_DETECT_ARGS + [
        f"--virtual-time-budget=20000",
        "--dump-dom",
        url
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    if result.returncode != 0:
        raise RuntimeError(f"Chrome 退出失败: {result.returncode}")
    html = result.stdout
    if not html or len(html) < 1000:
        raise RuntimeError("页面内容为空，可能网络或 Chrome 问题")
    return html


# ============================================================
# 2. HTML 解析 + 图片下载（一体化）
# ============================================================

def decode_html(text: str) -> str:
    """HTML 实体解码"""
    text = text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    text = text.replace('&#39;', "'").replace('&quot;', '"').replace('&nbsp;', ' ')
    text = text.replace('&ensp;', ' ').replace('&emsp;', ' ')
    return text


def download_one_image(url: str, fpath: str, cache_dir: str) -> str:
    """下载单张图片，返回本地文件名"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://mp.weixin.qq.com/'
    }
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
        with open(fpath, 'wb') as f:
            f.write(data)
        fname = os.path.basename(fpath)
        print(f"  [OK] {fname} ({len(data)//1024}KB)")
        return fpath
    except Exception as e:
        print(f"  [FAIL] {url[:60]}... → {e}")
        return None


def parse_and_scrape(html: str, cache_dir: str):
    """
    解析文章 HTML，返回：
    {
        'title': str,
        'author': str,
        'markdown': str,        # 含本地图片路径的完整 Markdown
        'blocks': [...],        # 原始内容块
        'local_images': [...]   # 本地图片路径列表（供飞书插入）
    }
    """
    # 找正文区域
    start = html.find('id="js_content"')
    if start == -1:
        start = html.find('rich_media_content')
    if start == -1:
        raise RuntimeError("无法定位文章正文区域（js_content）")
    
    end = html.find('id="js_pc_article_summary"', start)
    if end == -1:
        end = html.find('id="js_reward_section"', start)
    if end == -1:
        end = start + 1000000

    content = html[start:end]

    # 提取标题
    title_match = re.search(r'<title>(.*?)</title>', html)
    title = title_match.group(1).strip() if title_match else ""
    if title == "Weixin Official Accounts Platform" or not title:
        js_title = re.search(r"title\s*:\s*JsDecode\('([^']+)'\)", html)
        title = js_title.group(1) if js_title else "未命名文章"
    title = decode_html(title)

    # 提取作者
    author = ""
    author_match = re.search(r'id="js_name">([^<]+)<', content)
    if author_match:
        author = author_match.group(1).strip()

    # 提取所有 data-src 图片（保持顺序）
    img_pattern = re.compile(
        r'<img[^>]+data-src=["\']([^"\']+)["\'][^>]*>',
        re.IGNORECASE
    )

    blocks = []
    last_pos = 0
    img_counter = 0

    for m in img_pattern.finditer(content):
        url = decode_html(m.group(1))
        if 'data:image' in url or 'svg' in url.lower():
            continue
        url = urllib.parse.unquote(url)
        if 'mmbiz.qpic.cn' not in url:
            continue

        img_start = m.start()
        img_end = m.end()

        # 图片前的文字
        text_chunk = content[last_pos:img_start]
        text_clean = _clean_text(text_chunk)
        if len(text_clean) > 15:
            blocks.append({'type': 'text', 'content': text_clean})

        is_gif = '.gif' in url.lower() or '/mmbiz_gif/' in url

        # 下载图片
        img_counter += 1
        if is_gif:
            print(f"  [GIF] img_{img_counter:03d} (视频预览，跳过)")
            blocks.append({'type': 'video', 'url': url, 'local': None})
        else:
            fname = f"img_{img_counter:03d}.png"
            fpath = os.path.join(cache_dir, fname)
            local_path = download_one_image(url, fpath, cache_dir)
            blocks.append({'type': 'image', 'url': url, 'local': local_path})

        last_pos = img_end

    # 最后一段文字
    text_chunk = content[last_pos:]
    text_clean = _clean_text(text_chunk)
    if len(text_clean) > 15:
        blocks.append({'type': 'text', 'content': text_clean})

    # 生成 Markdown（含本地图片路径）
    markdown = _build_markdown(title, author, blocks)

    # 收集本地图片路径
    local_images = [b['local'] for b in blocks if b['type'] == 'image' and b['local']]

    return {
        'title': title,
        'author': author,
        'markdown': markdown,
        'blocks': blocks,
        'local_images': local_images,
    }


def _clean_text(html_chunk: str) -> str:
    """把 HTML 片段清洗成纯文字"""
    html_chunk = re.sub(r'<script[^>]*>.*?</script>', '', html_chunk, flags=re.DOTALL)
    html_chunk = re.sub(r'<style[^>]*>.*?</style>', '', html_chunk, flags=re.DOTALL)
    html_chunk = re.sub(r'<[^>]+>', ' ', html_chunk)
    html_chunk = decode_html(html_chunk)
    lines = [line.strip() for line in html_chunk.splitlines() if line.strip()]
    text = '\n'.join(lines)
    for kw in ['赞赏', '留言', '推荐阅读', '更多相关', '写出你的看法', '已无更多数据']:
        idx = text.find(kw)
        if 0 < idx < len(text) - 30:
            text = text[:idx]
    return text


def _build_markdown(title: str, author: str, blocks: list) -> str:
    """用内容块生成 Markdown（图片用本地路径）"""
    lines = []
    lines.append(f"# {title}\n")
    if author:
        lines.append(f"*来源：{author}*\n")
    lines.append("---\n")

    img_file_map = {}  # url -> local filename
    img_idx = 0
    for b in blocks:
        if b['type'] == 'text':
            lines.append(b['content'])
            lines.append("")
        elif b['type'] == 'image':
            img_idx += 1
            fname = f"img_{img_idx:03d}.png"
            lines.append(f"![{fname}]({fname})")
            img_file_map[b['url']] = fname
        elif b['type'] == 'video':
            lines.append("*（视频预览，已跳过）*")

    return '\n'.join(lines)


# ============================================================
# 3. 主流程
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="微信公众号文章抓取 + 飞书导入 v2.1")
    parser.add_argument("url", help="微信公众号文章链接")
    parser.add_argument("--title", help="自定义文档标题（默认从文章提取）")
    parser.add_argument("--author", help="自定义作者（默认从文章提取）")
    parser.add_argument("--cache-dir", help="图片缓存目录（默认 /tmp/wechat_article_XXXXXX）")
    parser.add_argument("--dry-run", action="store_true", help="仅解析不写入飞书")
    parser.add_argument("--output-json", action="store_true", help="输出 JSON 格式结果（含 markdown）供自动化调用")
    args = parser.parse_args()

    url = args.url.strip()
    
    # 自动生成带时间戳的缓存目录
    if args.cache_dir:
        cache_dir = args.cache_dir
    else:
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        cache_dir = f"/tmp/wechat_article_{ts}"
    os.makedirs(cache_dir, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"📱 微信公众号文章抓取 v2.1")
    print(f"{'='*60}")
    print(f"URL: {url}")
    print(f"缓存目录: {cache_dir}")
    print()

    # Step 1: 抓取 HTML
    print("📡 Step 1: 用 Chrome 抓取页面...")
    html = fetch_article_html(url)
    print(f"  HTML 大小: {len(html)//1024}KB")

    # Step 2: 解析 + 下载图片（一體化）
    print("🔍 Step 2: 解析文章结构 + 下载图片...")
    result = parse_and_scrape(html, cache_dir)
    
    print(f"\n  标题: {result['title']}")
    print(f"  作者: {result['author'] or '未知'}")
    print(f"  内容块: {len(result['blocks'])} 个")
    
    text_blocks = [b for b in result['blocks'] if b['type'] == 'text']
    img_blocks = [b for b in result['blocks'] if b['type'] == 'image']
    vid_blocks = [b for b in result['blocks'] if b['type'] == 'video']
    print(f"    - 文字段落: {len(text_blocks)}")
    print(f"    - 图片: {len(img_blocks)}（已下载）")
    print(f"    - 视频预览(GIF): {len(vid_blocks)}")

    # 输出摘要
    print(f"\n📋 内容摘要（前 3 段文字）:")
    for b in text_blocks[:3]:
        preview = b['content'][:100].replace('\n', ' ')
        print(f"  · {preview}...")

    if args.dry_run:
        print("\n🟡 Dry-run 模式，完成解析")
        return

    # 输出 JSON 格式（供自动化调用）
    if args.output_json:
        output = {
            'title': result['title'],
            'author': result['author'],
            'markdown': result['markdown'],
            'cache_dir': cache_dir,
            'local_images': result['local_images'],
            'blocks_count': len(result['blocks']),
        }
        print(f"\n__JSON_OUTPUT__: {json.dumps(output, ensure_ascii=False)}")
        return

    print(f"\n{'='*60}")
    print(f"✅ 抓取完成！")
    print(f"   标题: {result['title']}")
    print(f"   缓存目录: {cache_dir}")
    print(f"   本地图片: {len(result['local_images'])} 张")
    print(f"\n📄 Markdown 内容预览（前 500 字）:")
    print("-" * 40)
    print(result['markdown'][:500])
    print("-" * 40)
    print(f"\n{'='*60}")
    print("""
⚠️  飞书写入步骤（按顺序执行）：

    1. feishu_create_doc(title="标题") → 创建空白文档
    2. feishu_update_doc(mode=overwrite) → 写入 markdown 内容
    3. feishu_doc_media(insert) → 逐一插入所有本地图片（末尾追加）
    4. 用户在飞书编辑器中手动调整图片位置

⚠️  图片只能追加到文档末尾，这是飞书 API 限制。
""")


if __name__ == "__main__":
    main()
