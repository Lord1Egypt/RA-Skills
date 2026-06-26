#!/usr/bin/env python3
"""
工具函数模块 - 通用版本（安全修复版）
"""
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path


def get_config():
    """读取配置文件"""
    config_path = Path(__file__).parent.parent / "config.json"
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def ensure_browser_harness():
    """检查 Browser Harness 是否就绪"""
    try:
        result = subprocess.run(
            ["browser-harness", "--doctor"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return "daemon alive" in result.stdout or "[ok  ] daemon alive" in result.stdout
    except Exception:
        return False


def _run_browser_script(script_content, timeout=25):
    """安全地执行 browser-harness 脚本（避免 shell=True）"""
    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".py",
        prefix="bh_",
        delete=False
    ) as tmp:
        tmp.write(script_content)
        tmp_path = tmp.name

    try:
        with open(tmp_path, "r") as f:
            result = subprocess.run(
                ["browser-harness"],
                stdin=f,
                capture_output=True,
                text=True,
                timeout=timeout
            )
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return ""
    except Exception:
        return ""
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass


def extract_articles_generic(profile):
    """通用文章列表提取"""
    selectors = profile["selectors"]

    # 构建 JavaScript 提取代码
    article_row = selectors.get("article_row", "tr")
    title_sel = selectors.get("title", "td:nth-child(1)")
    date_sel = selectors.get("date", "td:nth-child(2)")
    link_sel = selectors.get("link", "a")
    next_page_sel = selectors.get("next_page", "")

    extract_js = f'''
Array.from(document.querySelectorAll("{article_row}")).map(row => {{
    const titleEl = row.querySelector("{title_sel}");
    const dateEl = row.querySelector("{date_sel}");
    const linkEl = row.querySelector("{link_sel}");
    if (!titleEl) return null;
    return {{
        title: titleEl.textContent.trim(),
        date: dateEl ? dateEl.textContent.trim() : "",
        link: linkEl ? (linkEl.href || linkEl.getAttribute("href")) : ""
    }};
}}).filter(a => a && a.title)
'''

    next_check_js = ""
    next_click_js = ""
    if next_page_sel:
        next_check_js = f'document.querySelector("{next_page_sel}") ? true : false'
        next_click_js = f'document.querySelector("{next_page_sel}").click()'

    script = f'''import json, time, socket

def send_cmd(js_code):
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.settimeout(10)
    sock.connect('/tmp/bu-default.sock')
    req = json.dumps({{"method": "Runtime.evaluate", "params": {{"expression": js_code, "returnByValue": True}}}})
    sock.sendall((req + '\\n').encode())
    resp = b''
    while True:
        chunk = sock.recv(8192)
        if not chunk:
            break
        resp += chunk
        if b'\\n' in resp:
            break
    sock.close()
    data = json.loads(resp.decode().strip())
    return data.get("result", {{}}).get("result", {{}}).get("value")

all_articles = []
page = 1
max_pages = 50

while page <= max_pages:
    articles_js = """{extract_js}"""
    articles = send_cmd(f"JSON.stringify({{articles_js}})")
    if articles:
        articles = json.loads(articles)
        if not articles:
            break
        all_articles.extend(articles)
    else:
        break
'''

    if next_page_sel:
        script += f'''
    has_next = send_cmd('{next_check_js}')
    if not has_next:
        break
    send_cmd('{next_click_js}')
    time.sleep(2)
    page += 1
'''
    else:
        script += '    break\n'

    script += '\nprint(json.dumps(all_articles, ensure_ascii=False))\n'

    try:
        output = _run_browser_script(script, timeout=120)
        if output:
            return json.loads(output)
        return []
    except Exception as e:
        print(f"提取失败: {e}")
        return []


def find_new_articles(articles, save_dir):
    """对比本地文件，找出新文章"""
    existing_files = list(save_dir.glob("*.md")) if save_dir.exists() else []
    existing_titles = set()

    for f in existing_files:
        name = f.stem
        parts = name.split("_", 1)
        if len(parts) > 1:
            existing_titles.add(parts[1])

    new_articles = []
    for article in articles:
        title = article["title"]
        matched = False
        for existing_title in existing_titles:
            if title in existing_title or existing_title in title:
                matched = True
                break
        if not matched:
            new_articles.append(article)

    return new_articles


def download_article_content_generic(article, save_dir, profile, config):
    """通用文章内容下载（安全版本）"""
    title = article["title"]
    date = article.get("date", "")
    link = article["link"]

    # 生成安全文件名
    safe_title = re.sub(r'[<>:"/\\|?*]', '', title)
    if date:
        filename = f"{date}_{safe_title}.md"
    else:
        filename = f"{safe_title}.md"
    filepath = save_dir / filename

    # 构建内容选择器
    content_selectors = profile.get("content_selectors", ["article", ".content"])
    selector_attempts = " || ".join(
        [f'document.querySelector("{sel}")?.innerText' for sel in content_selectors]
    )

    # 安全地转义 link 中的特殊字符
    safe_link = link.replace("'", "\\'").replace('"', '\\"')

    script = f"""goto('{safe_link}')
wait_for_load()
import time
time.sleep({profile.get("wait_after_load", 3)})
content = js('{selector_attempts} || document.body.innerText')
print(content)
"""

    try:
        content = _run_browser_script(script, timeout=25)

        if content and len(content) > 200 and "Traceback" not in content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"# {title}\n\n")
                if date:
                    f.write(f"**发布日期**: {date}\n\n")
                f.write(f"**原文链接**: {link}\n\n")
                f.write("---\n\n")
                f.write(content)
            return True
        return False
    except Exception:
        return False
