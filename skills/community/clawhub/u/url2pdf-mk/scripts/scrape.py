# -*- coding: utf-8 -*-
"""
微信文章抓取工具（url2pdf-mk）
支持 macOS / Windows / Linux
  • PDF：Chrome CDP 滚动加载 + 等待图片完成 + 浏览器原生打印
  • Markdown：按网页 DOM 顺序交叉输出文字和图片链接

用法：
  python3 scripts/scrape.py [URL]
  # 输出到 ~/Desktop/YYYY-MM-DD/{日期}_{标题}.pdf + .md
"""
import sys, os, re, time, subprocess, platform, base64, importlib.util
from datetime import date
SYSTEM = platform.system()  # 'Darwin' / 'Windows' / 'Linux'

# ═══════════════════════════════════════════════════════════════════════════
# 强制入口检查：禁止直接运行，必须由 main.py 启动
if os.environ.get('URL2PDFMK_ENTRY') != 'main':
    print("❌ 禁止直接运行 scrape.py，请通过 main.py 统一入口调用")
    print("   正确用法：py scripts/main.py <URL>")
    sys.exit(1)

# ═══════════════════════════════════════════════════════════════════════════
# 参数解析
import argparse
parser = argparse.ArgumentParser(description='单篇网页抓取：生成 PDF + Markdown')
parser.add_argument('url', nargs='?', help='目标 URL')
parser.add_argument('--isolated', action='store_true',
                    help='使用隔离浏览器 Profile（无 Cookie/登录态，适合公开内容）')
args = parser.parse_args()

TARGET_URL = args.url
ISOLATED_MODE = args.isolated

# ═══════════════════════════════════════════════════════════════════════════
# 0. 依赖
REQUIRED = ['websockets']
missing = [p for p in REQUIRED if importlib.util.find_spec(p) is None]
if missing:
    print(f"❌ 缺少依赖: {', '.join(missing)}")
    print(f"   请先安装: pip install {' '.join(missing)}")
    sys.exit(1)

# ═══════════════════════════════════════════════════════════════════════════
# 1. CDP 浏览器
# ─── 安全修复：仅使用本地脚本目录，不添加外部路径 ───────────────────────────
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
LOCAL_SCRIPTS = SKILL_DIR
sys.path.insert(0, LOCAL_SCRIPTS)

from browser_launcher import BrowserLauncher, BrowserNeedsCDPError
# ─── Monkey-patch：修复 Windows 上 proxy daemon thread 随父进程消亡后状态文件残留的问题 ───
# 根本原因：Windows 无 fork，proxy 以 daemon thread 运行，父进程退出时它也死，
# 但 proxy.json 还留着。导致下次 _try_existing_proxy 读到死 proxy → 健康检查失败 → 触发授权弹窗。
# 修复：如果 proxy.json 存在但进程已死，直接返回 None，让后续 HTTP 探测复用首次已授权的 CDP。
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

_orig_try_existing_proxy = None  # filled after import

try:
    from browser_launcher import _try_existing_proxy as _orig_try_existing_proxy
except ImportError:
    _orig_try_existing_proxy = None

def _fixed_try_existing_proxy(browser='chrome'):
    """Same as _try_existing_proxy, but on Windows: if proxy.json exists but the
    process is dead (daemon thread died with parent), clean up the state file
    and return None so we fall through to HTTP CDP probe (reusing first auth)."""
    state = _read_proxy_state()
    if state and not _proxy_process_alive(state):
        _cleanup_proxy_state()
        return None
    if _orig_try_existing_proxy:
        return _orig_try_existing_proxy(browser)
    return None

# Replace in browser_launcher module
import browser_launcher as _bl
_bl._try_existing_proxy = _fixed_try_existing_proxy
from cdp_client import CDPClient
from browser_actions import BrowserActions

# ─── 辅助 ─────────────────────────────────────────────────────────────────
def sanitize(name):
    return re.sub(r'[\\/:*?"<>|]', '', name).strip()[:80]

def parse_date(s):
    for pat in [r'(\d{4})[-/年](\d{1,2})[-/月](\d{1,2})',
                r'(\d{4})(\d{2})(\d{2})']:
        m = re.search(pat, s)
        if m:
            return f"{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"
    return None

# ═══════════════════════════════════════════════════════════════════════════
# 2. 启动浏览器
if not TARGET_URL:
    print("❌ 请提供 URL 参数：python3 scrape.py <URL>")
    sys.exit(1)

mode_str = "隔离模式（无 Cookie）" if ISOLATED_MODE else "复用 Profile（可访问登录态）"
print(f"🚀 启动浏览器（{mode_str}）...")
launcher = BrowserLauncher()
try:
    # 隔离模式：使用临时 Profile，不复用登录态
    cdp_url = launcher.launch(browser='chrome', reuse_profile=not ISOLATED_MODE)
except BrowserNeedsCDPError as e:
    print(f"⚠️  {e}")
    sys.exit(1)

client = CDPClient(cdp_url)
client.connect()

tabs = client.list_tabs()
tab = next((t for t in tabs if "mp.weixin.qq.com" in t.get('url', '')), None)
if tab:
    print("✅ 复用已有标签页")
    client.attach(tab['id'])
else:
    print("🌐 创建新标签页...")
    tab = client.create_tab(TARGET_URL)
    client.attach(tab['id'])

actions = BrowserActions(client, None)
print("⏳ 等待页面加载...")
# 【修正】timeout 单位是秒，不是毫秒
actions.wait_for_load(timeout=20.0)
time.sleep(4)

# ═══════════════════════════════════════════════════════════════════════════
# 3. 滚动 + 逐段小步滚动触发懒加载
print("📜 滚动加载全部内容...")
prev_h, stable = 0, 0
for i in range(1, 16):
    actions.evaluate(
        "window.scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'})")
    time.sleep(2.5)
    new_h = actions.evaluate("document.documentElement.scrollHeight")
    print(f"   轮次 {i:02d} — 高度 {new_h}px")
    if new_h == prev_h:
        stable += 1
        if stable >= 2:
            print("   页面已稳定")
            break
    else:
        stable = 0
    prev_h = new_h

# ─── 逐段小步滚动，触发懒加载 ──────────────────────────────────────────────
print("📜 逐段滚动触发懒加载...")
scroll_step = int(actions.evaluate("window.innerHeight"))
max_h = int(actions.evaluate("document.documentElement.scrollHeight"))
for y in range(0, max_h, scroll_step):
    actions.evaluate(f"window.scrollTo({{top: {y}, behavior: 'instant'}})")
    time.sleep(0.8)
actions.evaluate("window.scrollTo({top: 0, behavior: 'instant'})")
time.sleep(2)

# ─── 等待图片全部加载（轮询）────────────────────────────────────────────────
print("🖼️  等待所有图片加载完成...")
for attempt in range(1, 21):
    result = actions.evaluate("""
        (function() {
            var imgs = document.querySelectorAll('img');
            var pending = 0;
            imgs.forEach(function(img) {
                if (!img.complete || img.naturalWidth === 0) pending++;
            });
            return {pending: pending, total: imgs.length};
        })()
    """)
    print(f"   ⏳ 第 {attempt:02d} 次: {result['pending']}/{result['total']} 张未完成")
    if result['pending'] == 0:
        print("   ✅ 全部图片已加载完成")
        break
    time.sleep(2)
else:
    print(f"   ⚠️  仍有 {result['pending']} 张未完成，继续...")

time.sleep(2)

# ═══════════════════════════════════════════════════════════════════════════
# 4. 提取文章（JS DOM walk）
print("📝 提取文章内容...")
raw = actions.evaluate("""
(function() {
    var r = {};
    var t = document.querySelector('h1#activity-name') ||
            document.querySelector('meta[property="og:title"]') ||
            document.querySelector('title');
    r.title = t ? (t.content || t.textContent || '').trim() : '';
    var d = document.querySelector('meta[property="article:published_time"]') ||
            document.querySelector('em#publish_time') ||
            document.querySelector('span#publish_time');
    r.date = d ? (d.content || d.textContent || '').trim() : '';
    var a = document.querySelector('a#js_name') ||
            document.querySelector('meta[property="og:article:author"]') ||
            document.querySelector('#js_name');
    r.account = a ? (a.textContent || a.content || '').trim() : '';
    r.url = location.href;

    var b = document.getElementById('js_content') ||
            document.querySelector('#js_content') ||
            document.querySelector('.rich_media_content');
    r.bodyHTML = b ? b.innerHTML : '';

    // DOM walk：按顺序收集文字片段和图片
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
            // 【修正】优先取 data-src（懒加载真实地址），再取 src，再取 data-wap_src
            var src = node.getAttribute('data-src') ||
                      node.getAttribute('data-wap_src') ||
                      node.src || '';
            var isPh = src.startsWith('data:image/svg') ||
                       src.startsWith('data:image/gif;base64,iVBOR') ||
                       (src.length > 40000);
            if (src && !isPh && (src.startsWith('http') || src.startsWith('//'))) {
                if (src.startsWith('//')) src = 'https:' + src;
                fragments.push({type: 'img', src: src, alt: node.alt || ''});
            }
            return;
        }

        var child = node.firstChild;
        while (child) { walk(child); child = child.nextSibling; }

        if ({'p':1,'div':1,'section':1,'h1':1,'h2':1,'h3':1,'h4':1,
             'li':1,'blockquote':1,'br':1,'hr':1}.hasOwnProperty(tag)) {
            fragments.push({type: 'sep'});
        }
    }
    if (b) walk(b);
    r.fragments = fragments;
    return r;
})()
""")

title     = raw.get('title', '') or '无标题'
pub_date  = raw.get('date', '') or ''
account   = raw.get('account', '') or ''
fragments = raw.get('fragments', []) or []
page_url  = raw.get('url', '') or TARGET_URL

print(f"   标题:   {title}")
print(f"   日期:   {pub_date}")
print(f"   公众号: {account}")
print(f"   有效图片: {len([f for f in fragments if f['type'] == 'img'])} 张")

# ═══════════════════════════════════════════════════════════════════════════
# 5. 日期 & 目录
article_date = parse_date(pub_date) or date.today().isoformat()
today_date    = date.today().isoformat()
base_name    = sanitize(title)
file_name    = f"{article_date}_{base_name}"

desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
out_dir = os.path.join(desktop, today_date)
os.makedirs(out_dir, exist_ok=True)
print(f"📁 输出目录: {out_dir}")

# ═══════════════════════════════════════════════════════════════════════════
# 6. Markdown（按 DOM 顺序，图片穿插正文中）
md_lines = [
    f"# {title}",
    "",
    f"> **公众号:** {account}  ",
    f"> **发布日期:** {pub_date}  ",
    f"> **原文链接:** {page_url}",
    "",
    "---",
    "",
]

img_idx = 0
prev_was_img = False
for frag in fragments:
    if frag['type'] == 'text':
        text = frag['text'].strip()
        if text:
            md_lines.append(text)
            prev_was_img = False
    elif frag['type'] == 'img':
        src = frag.get('src', '') or ''
        if not src.startswith('http'):
            continue
        img_idx += 1
        alt = frag.get('alt', '').strip() or f'图片 {img_idx}'
        md_lines.append(f"**{alt}**")
        md_lines.append(f"![]({src})")
        md_lines.append("")
        prev_was_img = True
    elif frag['type'] == 'sep':
        if not prev_was_img:
            md_lines.append("")
        prev_was_img = False

md_text = '\n'.join(md_lines)
md_path = os.path.join(out_dir, f"{file_name}.md")
with open(md_path, 'w', encoding='utf-8') as f:
    f.write(md_text)
print(f"✅ Markdown: {md_path}  ({len(md_text)} 字符, {img_idx} 张图片)")

# ═══════════════════════════════════════════════════════════════════════════
# 7. PDF（浏览器原生打印）
pdf_path = os.path.join(out_dir, f"{file_name}.pdf")
print("🖨️  生成 PDF（浏览器原生打印，完整保留图片和样式）...")
time.sleep(1)

try:
    result = client.send('Page.printToPDF', {
        'paperWidth': 21.0 / 2.54,
        'paperHeight': 29.7 / 2.54,
        'marginTop': 1.0,
        'marginBottom': 1.0,
        'marginLeft': 1.0,
        'marginRight': 1.0,
        'printBackground': True,
        'scale': 1.0,
        'preferCSSPageSize': False,
    }, timeout=60)

    pdf_raw = result.get('data', '')
    pdf_bytes = base64.b64decode(pdf_raw) if isinstance(pdf_raw, str) else pdf_raw
    with open(pdf_path, 'wb') as f:
        f.write(pdf_bytes)
    print(f"✅ PDF:      {pdf_path}  ({len(pdf_bytes)//1024}KB)")

except Exception as e:
    print(f"⚠️  浏览器 PDF 打印失败: {e}")

# ═══════════════════════════════════════════════════════════════════════════
# 8. 关闭标签页（只关闭本次创建的标签，不关闭浏览器本身）
# 重要：调用 Browser.close 会关闭整个浏览器的 CDP 会话，导致 CDP Proxy
# 的上游连接断开，后续脚本无法复用授权状态而需要重新授权。
# 正确的做法是只关闭本次创建的标签页（Target.closeTarget）。
try:
    tab_id = tab.get('id')
    if tab_id:
        client.send('Target.closeTarget', {'targetId': tab_id})
        print("🔒 标签页已关闭（浏览器保持运行，授权状态保留）")
except Exception as e:
    print(f"⚠️  标签页关闭失败: {e}（可忽略，浏览器继续运行）")

# ═══════════════════════════════════════════════════════════════════════════
print("\n🎉 全部完成！")
print(f"   📄 Markdown → {md_path}")
print(f"   📕 PDF      → {pdf_path}")
print(f"   📁 目录     → {out_dir}")
