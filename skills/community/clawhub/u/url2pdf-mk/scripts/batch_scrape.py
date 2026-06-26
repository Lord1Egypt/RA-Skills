# -*- coding: utf-8 -*-
"""
批量抓取脚本：读取 xlsx 文件中的所有 URL，生成 PDF + Markdown
使用 OpenClaw 内置 CDP（通过 browser_launcher.py）
支持 macOS / Windows / Linux
"""
import sys, os, re, time, json, base64, subprocess, platform, importlib.util
from datetime import date

SYSTEM = platform.system()  # 'Darwin' / 'Windows' / 'Linux'

# ── 强制入口检查：禁止直接运行，必须由 main.py 启动 ─────────────────────────
if os.environ.get('URL2PDFMK_ENTRY') != 'main':
    print("❌ 禁止直接运行 batch_scrape.py，请通过 main.py 统一入口调用")
    print("   正确用法：py scripts/main.py <URL1> <URL2> ...")
    sys.exit(1)

# ── 参数解析 ──────────────────────────────────────────────────────────────
import argparse
parser = argparse.ArgumentParser(description='批量抓取网页生成 PDF + Markdown')
parser.add_argument('xlsx_path', nargs='?', help='xlsx 文件路径（包含 URL 列表）')
parser.add_argument('--isolated', action='store_true',
                    help='使用隔离浏览器 Profile（无 Cookie/登录态，适合公开内容）')
parser.add_argument('--output', '-o', help='输出目录（默认: ~/Desktop/当天日期）')
args = parser.parse_args()

# 移除硬编码路径：必须提供 xlsx 路径
if not args.xlsx_path:
    print("❌ 请提供 xlsx 文件路径")
    print("   用法: python3 batch_scrape.py <xlsx路径> [--isolated] [--output <目录>]")
    print("   示例: python3 batch_scrape.py ~/Desktop/urls.xlsx")
    sys.exit(1)

XLSX_PATH = os.path.abspath(os.path.expanduser(args.xlsx_path))
if not os.path.isfile(XLSX_PATH):
    print(f"❌ 文件不存在: {XLSX_PATH}")
    sys.exit(1)

OUT_DIR = os.path.abspath(os.path.expanduser(args.output)) if args.output else \
          os.path.expanduser(f'~/Desktop/{date.today().strftime("%Y-%m-%d")}')
os.makedirs(OUT_DIR, exist_ok=True)

# 隔离模式标志（传递给 browser_launcher）
ISOLATED_MODE = args.isolated

# ── 依赖（预装检查，不自动安装）─────────────────────────────────────────────
REQUIRED = ['openpyxl', 'websockets']
missing = [p for p in REQUIRED if importlib.util.find_spec(p) is None]
if missing:
    print(f"❌ 缺少依赖: {', '.join(missing)}")
    print(f"   请先安装: pip install {' '.join(missing)}")
    sys.exit(1)
import openpyxl

# ── CDP 模块路径 ───────────────────────────────────────────────────────────
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
LOCAL_SCRIPTS = SKILL_DIR   # 所有必要模块（cdp_proxy / cdp_client / browser_actions）均在此目录

# ── sys.path 安全收紧：仅添加本地脚本目录 ─────────────────────────────────
# ✅ 安全修复：不将任何外部目录加入 sys.path，所有模块从本地目录加载
sys.path.insert(0, LOCAL_SCRIPTS)

from browser_launcher import BrowserLauncher, BrowserNeedsCDPError

# ── Monkey-patch：修复 Windows 上 proxy daemon thread 随父进程消亡后状态文件残留的问题 ──
import json as _json, tempfile as _tempfile, getpass as _getpass
_PROXY_STATE_DIR = os.path.join(_tempfile.gettempdir(), f'cdp-proxy-{_getpass.getuser()}')
_PROXY_STATE_FILE = os.path.join(_PROXY_STATE_DIR, 'proxy.json')
_PROXY_PID_FILE   = os.path.join(_PROXY_STATE_DIR, 'proxy.pid')

def _read_proxy_state():
    if not os.path.isfile(_PROXY_STATE_FILE):
        return None
    try:
        with open(_PROXY_STATE_FILE, 'r') as f:
            return _json.load(f)
    except Exception:
        return None

def _proxy_process_alive(state):
    pid = state.get('pid')
    if not pid:
        return False
    try:
        os.kill(pid, 0)
        return True
    except (OSError, ProcessLookupError):
        return False

def _cleanup_proxy_state():
    for f in (_PROXY_STATE_FILE, _PROXY_PID_FILE):
        try:
            os.remove(f)
        except OSError:
            pass

_orig_try_existing_proxy = None
try:
    from browser_launcher import _try_existing_proxy as _orig_try_existing_proxy
except ImportError:
    _orig_try_existing_proxy = None

def _fixed_try_existing_proxy(browser='chrome'):
    state = _read_proxy_state()
    if state and not _proxy_process_alive(state):
        _cleanup_proxy_state()
        return None
    if _orig_try_existing_proxy:
        return _orig_try_existing_proxy(browser)
    return None

import browser_launcher as _bl
_bl._try_existing_proxy = _fixed_try_existing_proxy

from cdp_client import CDPClient
from browser_actions import BrowserActions

# ── 辅助函数 ────────────────────────────────────────────────────────────────
def sanitize(name):
    return re.sub(r'[\\/:*?"<>|]', '', name).strip()[:80]

def parse_date(s):
    for pat in [r'(\d{4})[-/年](\d{1,2})[-/月](\d{1,2})',
                r'(\d{4})(\d{2})(\d{2})']:
        m = re.search(pat, str(s))
        if m:
            return f"{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"
    return None

def scroll_and_wait(actions):
    """滚动页面触发懒加载，等待图片加载完成"""
    # 快速整页滚动
    actions.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(1)

    # 小步逐段滚动
    scroll_step = int(actions.evaluate("window.innerHeight"))
    max_h = int(actions.evaluate("document.documentElement.scrollHeight"))
    for y in range(0, max_h, scroll_step):
        actions.evaluate(f"window.scrollTo({{top: {y}, behavior: 'instant'}})")
        time.sleep(0.5)
    actions.evaluate("window.scrollTo({top: 0, behavior: 'instant'})")
    time.sleep(1)

    # 等待图片加载
    for _ in range(15):
        result = actions.evaluate("""
            (function() {
                var imgs = document.querySelectorAll('img');
                var pending = 0;
                imgs.forEach(function(img) {
                    if (!img.complete || img.naturalWidth === 0) pending++;
                });
                return pending;
            })()
        """)
        if result == 0:
            break
        time.sleep(2)

def extract_text_with_images(actions):
    """提取正文文本和图片链接"""
    return actions.evaluate("""
(function() {
    var r = {};
    var t = document.querySelector('h1#activity-name') ||
            document.querySelector('meta[property="og:title"]') ||
            document.querySelector('title');
    r.title = t ? (t.content || t.textContent || '').trim() : '';
    var d = document.querySelector('#publish_time') ||
            document.querySelector('em#publish_time') ||
            document.querySelector('span#publish_time') ||
            document.querySelector('meta[property="article:published_time"]');
    r.date = d ? (d.content || d.textContent || '').trim() : '';
    var a = document.querySelector('#js_name') ||
            document.querySelector('a#js_name') ||
            document.querySelector('.rich_media_meta_list');
    r.author = a ? (a.textContent || '').trim() : '';

    var b = document.getElementById('js_content') ||
            document.querySelector('#js_content') ||
            document.querySelector('.rich_media_content');

    var fragments = [];
    function walk(node) {
        if (!node) return;
        if (node.nodeType === Node.TEXT_NODE) {
            var t = (node.textContent || '').replace(/[\\s\\n]+/g, ' ').trim();
            if (t.length > 1) fragments.push({type: 'text', text: t});
            return;
        }
        if (node.nodeType !== Node.ELEMENT_NODE) return;
        var tag = (node.tagName || '').toLowerCase();
        if ({'script':1,'style':1,'noscript':1,'head':1,'iframe':1,
             'audio':1,'video':1,'canvas':1,'svg':1,'form':1}.hasOwnProperty(tag)) return;

        if (tag === 'img') {
            // 优先 data-src（懒加载），再 src
            var src = node.getAttribute('data-src') ||
                      node.getAttribute('data-wap_src') ||
                      node.src || '';
            var isPh = src.startsWith('data:image/svg') ||
                       (src.length > 40000);
            if (src && !isPh && (src.startsWith('http') || src.startsWith('//'))) {
                if (src.startsWith('//')) src = 'https:' + src;
                fragments.push({type: 'img', src: src});
            }
            return;
        }
        var child = node.firstChild;
        while (child) { walk(child); child = child.nextSibling; }
        if ({'p':1,'div':1,'section':1,'h1':1,'h2':1,'h3':1,'h4':1,
             'li':1,'blockquote':1,'br':1}.hasOwnProperty(tag)) {
            fragments.push({type: 'sep'});
        }
    }
    if (b) walk(b);
    r.fragments = fragments;
    return r;
})()
""")

# ── 主程序 ─────────────────────────────────────────────────────────────────
def main():
    # 读取 Excel
    wb = openpyxl.load_workbook(XLSX_PATH)
    ws = wb.active
    rows = list(ws.iter_rows(min_row=2, values_only=True))
    total = len(rows)
    print(f"共读取 {total} 条记录")

    # ── 整个批量过程只启动一次浏览器 ──────────────────────────────────────
    mode_str = "隔离模式（无 Cookie）" if ISOLATED_MODE else "复用 Profile（可访问登录态）"
    print(f"🚀 启动浏览器（{mode_str}）...")
    launcher = BrowserLauncher()
    try:
        # 隔离模式：使用临时 Profile，不复用登录态
        cdp_url = launcher.launch(browser='chrome', reuse_profile=not ISOLATED_MODE)
    except BrowserNeedsCDPError as e:
        print(f"⚠️  {e}")
        return

    client = CDPClient(cdp_url)
    client.connect()
    actions = BrowserActions(client, None)

    success, failed = 0, []

    for i, row in enumerate(rows, 1):
        title    = str(row[1]).strip() if row[1] else f"文章{i}"
        url      = str(row[5]).strip() if row[5] else ''
        date_val = row[2]

        if not url or not url.startswith('http'):
            print(f"[{i}/{total}] 跳过（无URL）: {title[:40]}")
            continue

        safe_title  = sanitize(title)
        pub_date    = parse_date(date_val) or 'unknown'
        print(f"[{i}/{total}] 处理: {title[:40]}")

        tab = None  # 避免异常时 tab 未定义
        try:
            # 打开页面
            tab = client.create_tab(url)
            client.attach(tab['id'])
            actions.wait_for_load(timeout=20.0)
            time.sleep(3)

            # 滚动加载
            scroll_and_wait(actions)

            # 提取内容
            data = extract_text_with_images(actions)
            effective_date = parse_date(data.get('date', '')) or pub_date
            author = data.get('author', '') or '复旦大学附属妇产科医院'
            fragments = data.get('fragments', [])

            # 用网页获取的真实标题覆盖 xlsx 中的标题，用于文件名
            web_title = data.get('title', '')
            if web_title:
                title = web_title
                safe_title = sanitize(title)

            # ── Markdown ──────────────────────────────────────────────
            md_lines = [
                f"# {title}",
                "",
                f"> **公众号:** {author}",
                f"> **发布日期:** {effective_date}",
                f"> **原文链接:** {url}",
                "",
                "---",
                "",
            ]
            img_idx, prev_was_img = 0, False
            for frag in fragments:
                if frag['type'] == 'text':
                    text = frag['text'].strip()
                    if text:
                        md_lines.append(text)
                        prev_was_img = False
                elif frag['type'] == 'img':
                    src = frag.get('src', '')
                    if not src.startswith('http'):
                        continue
                    img_idx += 1
                    md_lines.append(f"**图片 {img_idx}**")
                    md_lines.append(f"![]({src})")
                    md_lines.append("")
                    prev_was_img = True
                elif frag['type'] == 'sep' and not prev_was_img:
                    md_lines.append("")
                    prev_was_img = False

            md_filename = f"{effective_date}_{safe_title}.md"
            md_path = os.path.join(OUT_DIR, md_filename)
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(md_lines))
            print(f"  ✅ Markdown: {md_filename} ({img_idx} 张图片)")

            # ── PDF ─────────────────────────────────────────────────
            pdf_filename = f"{effective_date}_{safe_title}.pdf"
            pdf_path = os.path.join(OUT_DIR, pdf_filename)
            result = client.send('Page.printToPDF', {
                'printBackground': True,
                'paperWidth': 21.0 / 2.54,
                'paperHeight': 29.7 / 2.54,
                'marginTop': 1.0,
                'marginBottom': 1.0,
                'marginLeft': 1.0,
                'marginRight': 1.0,
                'scale': 1.0,
                'preferCSSPageSize': False,
            }, timeout=60)
            pdf_data = base64.b64decode(result.get('data', ''))
            with open(pdf_path, 'wb') as f:
                f.write(pdf_data)
            print(f"  ✅ PDF:      {pdf_filename} ({len(pdf_data)//1024}KB)")

            # ── 只关闭标签页，保持浏览器运行（授权状态复用）──────────────
            tab_id = tab.get('id')
            if tab_id:
                try:
                    client.send('Target.closeTarget', {'targetId': tab_id})
                except Exception:
                    pass
            client.detach()
            success += 1
            print()
            time.sleep(1)

        except Exception as e:
            print(f"  ❌ 失败: {e}")
            failed.append((i, title, url))
            # 出错时也只关闭标签页，不断开连接
            if tab is not None:
                try:
                    tab_id = tab.get('id')
                    if tab_id:
                        client.send('Target.closeTarget', {'targetId': tab_id})
                except Exception:
                    pass
            try:
                client.detach()
            except Exception:
                pass
            continue

    # ── 不调用 client.close()，让浏览器保持运行 ──────────────────────────
    print(f"\n{'='*50}")
    print(f"完成！")
    print(f"  成功: {success} 篇")
    if failed:
        print(f"  失败: {len(failed)} 篇")
        for _, t, u in failed:
            print(f"    - {t}: {u[:60]}")
    print(f"输出目录: {OUT_DIR}")
    print(f"浏览器保持运行中，下次脚本会自动复用授权，无需重新授权！")

if __name__ == '__main__':
    main()
