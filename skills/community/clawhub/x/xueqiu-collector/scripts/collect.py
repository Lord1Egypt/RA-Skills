"""
雪球帖子全量采集脚本（通用 Skill 版）
========================================
功能：
  1. 采集任意雪球用户的全部帖子
  2. 完整正文提取 + Markdown 格式化
  3. 图片下载 + OCR 识别（winocr/tesseract）
  4. V4 规则分析（零 token 消耗）
     - 帖子类型 / 投资相关性 / 情感 / 操作意图 / 主题标签 / 质量评分
  5. SQLite 数据库持久化 + JSON/Markdown 备份输出

反爬虫机制：
  - 随机延迟 2-5 秒，每 20 条强制休息 8-12 秒
  - 失败重试最多 3 次，指数退避
  - 自动检测 429 限流错误
  - 连续 N 页无新帖自动停止列表扫描

使用方式：
  # 增量采集（推荐）
  py scripts/collect.py --author "昵称" --url "https://xueqiu.com/u/7712999844" --db "data.db"

  # 强制扫描列表找新帖
  py scripts/collect.py --author "昵称" --url "https://xueqiu.com/u/7712999844" --refresh-list

  # 强制重新采集正文
  py scripts/collect.py --author "昵称" --url "https://xueqiu.com/u/7712999844" --force-collect

  # 只采最新 N 条
  py scripts/collect.py --author "昵称" --url "https://xueqiu.com/u/7712999844" --force-collect --latest --limit 10

依赖：
  - playwright-cli（npx）已安装
  - Edge 浏览器 + 真实 Profile（带登录态）
  - Python 3.10+
"""

import subprocess
import sys
import os
import time
import re
import json
import sqlite3
import random
import urllib.request
import urllib.parse
from datetime import datetime, timedelta
from pathlib import Path


# ════════════════════════════════════════
#  参数解析 & 配置初始化
# ════════════════════════════════════════

def parse_args():
    """解析命令行参数，缺省参数时交互式引导用户输入"""
    import argparse
    p = argparse.ArgumentParser(
        description="雪球帖子全量采集（V4 规则分析版）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  py scripts/collect.py --author "随缘的人生体验" --url "https://xueqiu.com/u/7712999844"
  py scripts/collect.py --author "用户名" --url "URL" --db "my_data.db" --out-dir "./output"
  py scripts/collect.py --author "用户名" --url "URL" --force-collect --latest --limit 10

首次使用提示：
  不传 --author / --url 时会交互式引导输入，无需记忆命令格式。
        """
    )
    p.add_argument('--author', default=None, help='发帖人昵称')
    p.add_argument('--url', default=None, help='雪球主页 URL (https://xueqiu.com/u/XXXXXX)')
    p.add_argument('--db', default=None, help='SQLite 数据库路径（默认: <脚本目录>/../data/xueqiu.db）')
    p.add_argument('--out-dir', default=None, help='数据输出根目录（默认: <脚本目录>/../data/xueqiu）')
    p.add_argument('--npx', default=None, help='npx 可执行路径（自动探测）')
    p.add_argument('--edge-profile', default=None, help='Edge Profile 路径（自动探测 Windows 默认）')
    p.add_argument('--refresh-list', action='store_true', help='强制扫描列表页查找新帖')
    p.add_argument('--force-collect', action='store_true', help='强制重新采集正文（跳过列表扫描）')
    p.add_argument('--latest', action='store_true', help='按最新优先排序采集')
    p.add_argument('--limit', type=int, default=0, help='限制采集数量（0 = 全部）')
    p.add_argument('--stop-on-no-new', type=int, default=3, help='连续多少页无新帖后停止（默认 3）')
    return p.parse_args()


def resolve_config(args):
    """将命令行参数补全为完整配置字典（缺省参数时交互式引导输入）"""

    # ── 首次使用：交互式引导 ──
    if not args.author or not args.url:
        print()
        print("═" * 50)
        print("  🧊 雪球帖子采集 — 首次运行配置向导")
        print("═" * 50)
        print()

    if not args.author:
        author = input("  📝 请输入发帖人昵称（如: 随缘的人生体验）: ").strip()
        while not author:
            author = input("  ⚠️ 昵称不能为空，请重新输入: ").strip()
        args.author = author

    if not args.url:
        print()
        print(f"  📌 正在采集 [{args.author}] 的帖子")
        print(f"  💡 格式: https://xueqiu.com/u/用户ID（从雪球主页地址栏复制）")
        url = input("  🔗 请输入雪球主页 URL: ").strip()
        while not url or 'xueqiu.com' not in url.lower():
            url = input("  ⚠️ 请输入正确的雪球 URL (含 xueqiu.com): ").strip()
        args.url = url.strip('/')

    if not args.db and not args.out_dir:
        print()
        print(f"  ✅ 配置完成！昵称={args.author}")
        print(f"     URL: {args.url}")
        print()

    # 脚本所在目录
    _skill_dir = Path(__file__).resolve().parent
    _root = _skill_dir.parent  # Skill 根目录

    # ── npx 路径 ──
    npx = args.npx or find_npx()
    if not npx:
        print("❌ 找不到 npx 命令，请安装 Node.js 或用 --npx 指定路径")
        sys.exit(1)

    # ── Edge Profile ──
    edge_profile = args.edge_profile or detect_edge_profile()

    # ── 数据库 ──
    db_path = args.db or str(_root / 'data' / 'xueqiu.db')

    # ── 输出目录 ──
    out_root = args.out_dir or str(_root / 'data' / 'xueqiu')

    # ── 日志 ──
    log_dir = str(_root / 'logs')
    log_path = os.path.join(log_dir, 'xueqiu_collect.log')

    return {
        'npx': npx,
        'edge_profile': edge_profile,
        'db_path': db_path,
        'out_root': out_root,
        'log_path': log_path,
        'snap_dir': str(_root / '.playwright-cli'),
        'args': args,
    }


def find_npx():
    """自动探测 npx 可执行路径"""
    candidates = [
        'npx',
        os.path.join(os.environ.get('APPDATA', ''), '..', 'nodejs', 'npx.cmd'),
        os.path.join(os.environ.get('LOCALAPPDATA', ''), 'nodejs', 'npx.cmd'),
        r'C:\Users\123\nodejs\npx.cmd',
    ]
    for c in candidates:
        try:
            result = subprocess.run([c, '--version'], capture_output=True, timeout=5)
            if result.returncode == 0:
                return c if os.path.isabs(c) else shutil_which(c) or c
        except Exception:
            continue
    return None


def detect_edge_profile():
    """自动探测 Edge Profile 路径"""
    local_app = os.environ.get('LOCALAPPDATA', '')
    profile = os.path.join(local_app, r'Microsoft\Edge\User Data\Default')
    if os.path.isdir(profile):
        return profile
    # 回退到通用路径
    return os.path.expandvars(r'%LOCALAPPDATA%\Microsoft\Edge\User Data\Default')


def shutil_which(name):
    """跨平台 which 实现"""
    try:
        import shutil
        return shutil.which(name)
    except ImportError:
        return None


# ── UTF-8 输出 ──
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')


# ════════════════════════════════════════
#  反爬虫配置
# ════════════════════════════════════════

REAL_USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
]

MIN_DELAY      = 2.0   # 最小延迟（秒）
MAX_DELAY      = 5.0   # 最大延迟（秒）
ERROR_DELAY    = 8.0   # 错误后延迟（秒）
MAX_RETRIES    = 3      # 最大重试次数
REQUEST_INTERVAL = 3.0  # 列表页请求间隔（秒）


class _Tee:
    """stdout 双写：终端 + 日志文件"""
    def __init__(self, stream, logpath):
        self._stream = stream
        os.makedirs(os.path.dirname(logpath), exist_ok=True)
        self._log = open(logpath, 'w', encoding='utf-8', buffering=1)

    def write(self, data):
        self._stream.write(data)
        self._stream.flush()
        self._log.write(data)
        self._log.flush()

    def flush(self):
        self._stream.flush()
        self._log.flush()

    def reconfigure(self, **kwargs):
        pass


# ════════════════════════════════════════
#  分类关键词表（可自定义）
# ════════════════════════════════════════

CATEGORY_KEYWORDS = {
    "腾讯控股":   ["腾讯", "TX", "00700", "微信", "微视", "企鹅"],
    "华晨中国":   ["华晨", "华晨中国", "01114", "宝马"],
    "小赢科技":   ["小赢", "XW", "XY"],
    "珩湾科技":   ["珩湾"],
    "江南布衣":   ["江南布衣", "JNBY", "03306"],
    "英美烟草":   ["英美烟草", "BTI", "BAT"],
    "唯品会":     ["唯品会", "VIPS"],
    "百度":       ["百度", "BIDU", "09888"],
    "阿里巴巴":   ["阿里", "阿里巴巴", "BABA", "09988"],
    "美团":       ["美团", "03690"],
    "京东":       ["京东", "JD", "09618"],
    "比亚迪":     ["比亚迪", "BYD", "01211"],
    "招商银行":   ["招行", "招商银行", "03968"],
    "贵州茅台":   ["茅台", "600519"],
    "港股通用":   ["港股", "恒生", "H股"],
    "美股通用":   ["美股", "纳斯达克"],
    "A股通用":    ["A股", "沪深", "创业板"],
    "ETF/基金":   ["ETF", "基金"],
    "宏观分析":   ["宏观", "美联储", "加息", "降息", "通胀", "GDP"],
    "市场观点":   ["大盘", "行情", "市场", "估值", "牛市", "熊市"],
    "操作日记":   ["仓位", "建仓", "加仓", "减仓", "清仓", "止损"],
    "读书笔记":   ["读书", "笔记", "推荐", "书单"],
    "生活随笔":   ["生活", "随笔", "感悟", "日记"],
}
FALLBACK_CATEGORY = "其他"


# ════════════════════════════════════════
#  playwright-cli 工具函数
# ════════════════════════════════════════

def run_cmd(cfg, args_list, timeout=30, retries=0, no_delay=False):
    """执行 playwright-cli 命令，带反爬机制"""
    npx = cfg['npx']
    session = "xueqiu_full"

    for attempt in range(retries + 1):
        try:
            if attempt == 0 and not no_delay:
                time.sleep(random.uniform(MIN_DELAY, MAX_DELAY))

            result = subprocess.run(
                [npx, "playwright-cli", f"-s={session}"] + args_list,
                capture_output=True, text=True, encoding="utf-8",
                errors="replace", timeout=timeout
            )
            stdout, stderr = result.stdout.strip(), result.stderr.strip()

            if "429" in stderr or "Too Many Requests" in stdout:
                if attempt < retries:
                    wait_time = ERROR_DELAY * (attempt + 1)
                    print(f"    [限流] 等待 {wait_time:.1f}s 后重试...")
                    time.sleep(wait_time)
                    continue
                return stdout, stderr

            if not stdout and not stderr:
                if attempt < retries:
                    print(f"    [重试] 空输出 {attempt+1}/{retries}")
                    time.sleep(2)
                    continue

            return stdout, stderr

        except subprocess.TimeoutExpired:
            if attempt < retries:
                print(f"    [超时] 重试 {attempt+1}/{retries}")
                time.sleep(3)
                continue
            return "", "Timeout"
        except Exception as e:
            if attempt < retries:
                print(f"    [异常] {e}，重试 {attempt+1}/{retries}")
                time.sleep(2)
                continue
            return "", str(e)

    return "", "Max retries exceeded"


def ensure_browser_open(cfg, target_url):
    """确保浏览器在线并导航到目标 URL"""
    npx = cfg['npx']
    edge_profile = cfg['edge_profile']
    session = "xueqiu_full"

    for attempt in range(3):
        out, err = run_cmd(cfg, ["snapshot"], timeout=10, retries=1)
        if "Page URL" in out:
            print("  浏览器已在线")
            run_cmd(cfg, ["goto", target_url], timeout=30, no_delay=True)
            time.sleep(2)
            return

        print(f"  [尝试 {attempt+1}/3] 启动 Edge 浏览器...")
        subprocess.Popen(
            [npx, "playwright-cli", f"-s={session}", "open", target_url,
             "--browser=msedge", "--headed", f"--profile={edge_profile}"],
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
        time.sleep(random.uniform(6, 9))

    print("  浏览器已启动")


def take_snapshot(cfg):
    """获取页面快照并返回路径"""
    snap_dir = cfg['snap_dir']
    out, err = run_cmd(cfg, ["snapshot"], timeout=30, no_delay=True)
    time.sleep(0.3)

    match = re.search(r'\[Snapshot\]\(([^)]+\.yml)\)', out)
    if match:
        path = match.group(1)
        return path if os.path.isabs(path) else os.path.abspath(path)

    ymls = sorted([
        f for f in os.listdir(snap_dir)
        if f.startswith("page-") and f.endswith(".yml")
    ], reverse=True)
    return os.path.join(snap_dir, ymls[0]) if ymls else None


def find_next_page_ref(snap_file):
    with open(snap_file, encoding='utf-8', errors='replace') as f:
        content = f.read()
    m = re.search(r'link "下一页".*?\[ref=(e\d+)\]', content)
    return m.group(1) if m else None


# ════════════════════════════════════════
#  时间解析
# ════════════════════════════════════════

def parse_xueqiu_time(raw):
    """将雪球时间文本解析为 YYYY-MM-DD 格式"""
    if not raw:
        return ""
    now = datetime.now()
    clean = raw.split('·')[0].strip().replace('修改于', '').replace('发布于', '').strip()

    m = re.match(r'(\d{4})-(\d{2})-(\d{2})', clean)
    if m: return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    if clean.startswith('今天'): return now.strftime('%Y-%m-%d')
    if clean.startswith('昨天'): return (now - timedelta(days=1)).strftime('%Y-%m-%d')
    if clean.startswith('前天'): return (now - timedelta(days=2)).strftime('%Y-%m-%d')

    m = re.match(r'(\d+)\s*(分钟前|小时前)', clean)
    if m: return now.strftime('%Y-%m-%d')

    m = re.match(r'(\d+)\s*天前', clean)
    if m: return (now - timedelta(days=int(m.group(1)))).strftime('%Y-%m-%d')

    m = re.match(r'(\d{2})-(\d{2})', clean)
    if m:
        month, day = int(m.group(1)), int(m.group(2))
        year = now.year if month <= now.month else now.year - 1
        return f"{year:04d}-{month:02d}-{day:02d}"
    return raw


# ════════════════════════════════════════
#  图片处理（下载 + OCR）
# ════════════════════════════════════════

def extract_images_from_page(cfg):
    """从当前页面 DOM 提取 article 区域图片"""
    js_code = (
        '() => { var a = document.querySelector("article"); if (!a) return []; '
        'var imgs = a.querySelectorAll("img"); var r = []; '
        'var skip = ["实盘认证","认证","微信分享","icon","fold","点赞","收藏"]; '
        'for (var i = 0; i < imgs.length; i++) { '
        'var im = imgs[i]; var src = im.src || ""; var alt = (im.alt || "").trim(); '
        'if (!src || src.indexOf("data:") === 0 || src.indexOf(".svg") > -1) continue; '
        'if (im.naturalWidth < 100 && im.naturalHeight < 100) continue; '
        'if (alt.charAt(0) === "[" && alt.charAt(alt.length - 1) === "]") continue; '
        'var skipIt = false; for (var s = 0; s < skip.length; s++) { '
        'if (alt.indexOf(skip[s]) > -1) { skipIt = true; break; } } '
        'if (skipIt) continue; '
        'if (src.indexOf("http") !== 0) continue; '
        'r.push({alt: alt, src: src}); } return r; }'
    )
    out, err = run_cmd(cfg, ["eval", js_code], timeout=15)
    if not out:
        return []

    m = re.search(r'### Result\s*\n(.*?)\n### Ran Playwright code', out, re.DOTALL)
    json_str = m.group(1).strip() if m else out
    try:
        results = json.loads(json_str)
        return results if isinstance(results, list) else []
    except (json.JSONDecodeError, TypeError):
        return []


def download_images(image_list, post_id, images_dir):
    """下载图片到本地"""
    if not image_list:
        return []
    os.makedirs(images_dir, exist_ok=True)
    results = []
    ua = random.choice(REAL_USER_AGENTS)
    headers = {'User-Agent': ua, 'Referer': 'https://xueqiu.com/'}

    for i, img_info in enumerate(image_list):
        src = img_info.get('src', '')
        alt = img_info.get('alt', '')
        if not src:
            results.append({**img_info, 'local_path': None, 'success': False})
            continue

        parsed = urllib.parse.urlparse(src)
        ext = '.png' if '.png' in parsed.path else ('.gif' if '.gif' in parsed.path else '.jpg')
        filename = f"{post_id}_{i+1}{ext}"
        local_path = os.path.join(images_dir, filename)

        if os.path.exists(local_path) and os.path.getsize(local_path) > 100:
            results.append({**img_info, 'local_path': local_path, 'success': True})
            continue

        try:
            req = urllib.request.Request(src, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = resp.read()
                if len(data) < 100:
                    results.append({**img_info, 'local_path': None, 'success': False})
                    continue
                with open(local_path, 'wb') as f:
                    f.write(data)
                results.append({**img_info, 'local_path': local_path, 'success': True})
        except Exception as e:
            print(f"    [图片下载失败] {alt[:20]}: {e}")
            results.append({**img_info, 'local_path': None, 'success': False})

    return results


def ocr_image(image_path):
    """OCR 单张图片（winocr > tesseract）"""
    if not os.path.exists(image_path):
        return ""
    try:
        import winocr
        from PIL import Image as _PILImage
        im = _PILImage.open(image_path)
        r = winocr.recognize_pil_sync(im, 'zh-Hans')
        text = r.get('text', '').strip() if isinstance(r, dict) else ''
        if text: return text
        r2 = winocr.recognize_pil_sync(im, 'en-US')
        text2 = r2.get('text', '').strip() if isinstance(r2, dict) else ''
        if text2: return text2
    except ImportError:
        pass
    except Exception:
        pass
    try:
        res = subprocess.run(
            ["tesseract", image_path, "-", "-l", "chi_sim+eng", "--psm", "3"],
            capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=30
        )
        if res.stdout.strip():
            return res.stdout.strip()
    except FileNotFoundError:
        pass
    except Exception:
        pass
    return ""


def ocr_post_images(post_id, images_dir):
    """对帖子所有图片做 OCR"""
    if not os.path.isdir(images_dir):
        return ""
    all_images = sorted([
        f for f in os.listdir(images_dir)
        if f.startswith(f"{post_id}_") and not f.endswith('.txt')
    ])
    if not all_images:
        return ""
    results = []
    for fname in all_images:
        text = ocr_image(os.path.join(images_dir, fname))
        if text:
            results.append(f"[图{fname}]\n{text}")
    return "\n\n---\n\n".join(results)


def update_images_in_markdown(md_content, image_results):
    """将已下载图片嵌入 Markdown 内容"""
    if not image_results:
        return md_content
    appended = []
    for img in image_results:
        if not img.get('success') or not img.get('local_path'):
            continue
        alt = img.get('alt', '')
        abs_path = os.path.abspath(img['local_path']).replace('\\', '/')
        if alt:
            placeholder, replacement = f'![{alt}]', f'![{alt}]({abs_path})'
            if placeholder in md_content:
                md_content = md_content.replace(placeholder, replacement)
                continue
        label = alt if alt else 'image'
        appended.append(f'![{label}]({abs_path})')

    if appended:
        md_content = re.sub(r'\n*!\[image\]\([^)]+\)', '', md_content)
        md_content = md_content.rstrip() + '\n\n' + '\n\n'.join(appended)
    return md_content


# ════════════════════════════════════════
#  正文提取（从快照解析 YML → Markdown）
# ════════════════════════════════════════

def extract_full_content_from_snap(snap_file):
    """从帖子详情页快照提取完整正文 Markdown，返回 (md_text, reply_to_post_id, raw_time)"""
    with open(snap_file, encoding='utf-8', errors='replace') as f:
        content = f.read()

    raw_time = ""
    time_match = re.search(
        r'link\s+"([^"]*?\d{1,2}[-/:]\d{1,2}(?:\s*\d{1,2}:\d{1,2})?[^"]*?·\s*来自[^"]+)"',
        content
    )
    if time_match:
        raw_time = time_match.group(1)

    article_match = re.search(
        r'- article \[ref=\w+\]:(.*?)(?=\n        - (?:generic|heading) \[ref=\w+\].*?(?:热门话题|全部讨论|回复@|点赞|收藏$))',
        content, re.DOTALL
    )
    if not article_match:
        article_match = re.search(r'- article \[ref=\w+\]:(.*?)(?=\n      - generic \[ref=\w+\]:\n)', content, re.DOTALL)
    if not article_match:
        article_match = re.search(r'- article \[ref=\w+\]:(.*)', content, re.DOTALL)
    if not article_match:
        return "", "", raw_time

    article_text = article_match.group(1)

    SKIP_WORDS = {
        '转发', '评论', '赞', '收藏', '分享', '举报', '关注', '取消关注',
        '回复', '查看对话', '展开', '加载中', '更多', '置顶',
        '转载', '原文', '来源', '编辑', '删除', '修改',
        '风险提示：用户发表的所有文章仅代表个人观点，与雪球的立场无关。',
        '微信分享', '发布', '仅在正文下讨论', '实盘认证', '认证',
    }

    lines = article_text.strip().split('\n')
    md_lines, current_segment = [], []
    in_blockquote, blockquote_indent = False, 0
    reply_to_post_id, pending_link_check = "", False

    def flush_segment():
        nonlocal current_segment
        if current_segment:
            text = ''.join(current_segment).strip()
            if text and text not in SKIP_WORDS and len(text) >= 2:
                if in_blockquote:
                    md_lines.append('> ' + text)
                else:
                    md_lines.append(text)
            current_segment = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        line_indent = len(line) - len(line.lstrip())

        if pending_link_check and stripped.startswith('- /url:'):
            url_val = stripped.replace('- /url:', '').strip().strip('"')
            if in_blockquote and not reply_to_post_id:
                m = re.search(r'/\d+/(\d+)#comment', url_val)
                if m:
                    reply_to_post_id = m.group(1)
            pending_link_check = False
            continue
        pending_link_check = False

        if in_blockquote and line_indent <= blockquote_indent:
            flush_segment()
            in_blockquote = False
            md_lines.append('')
        if any(kw in stripped for kw in ['点赞', '收藏', '回复@', '转发"', '讨论"', '删除']):
            break

        heading_match = re.match(r'- heading(?:\s+"(.+?)")?\s*\[level=(\d+)\]', stripped)
        if heading_match:
            flush_segment()
            level = int(heading_match.group(2))
            title = heading_match.group(1) or ''
            if title and title not in SKIP_WORDS:
                md_lines.append('')
                md_lines.append('#' * min(level, 4) + ' ' + title.strip('"'))
                md_lines.append('')
            continue

        if re.match(r'- blockquote\b', stripped):
            flush_segment()
            in_blockquote = True
            blockquote_indent = line_indent
            md_lines.append('')
            md_lines.append('> **引用：**')
            continue

        para_match = re.match(r'- paragraph\b.*?:\s*(.*)', stripped)
        if para_match:
            flush_segment()
            text = para_match.group(1).strip().strip('"')
            if text and text not in SKIP_WORDS and len(text) >= 2:
                md_lines.append(('> ' if in_blockquote else '') + text)
            continue

        text_match = re.match(r'- text:\s*(.*)', stripped)
        if text_match:
            text = text_match.group(1).strip().strip('"')
            if text and text not in SKIP_WORDS:
                current_segment.append(text)
            continue

        img_match = re.match(r'- img(?:\s+"(.+?)")?', stripped)
        if img_match:
            flush_segment()
            alt = img_match.group(1) or ''
            if alt.startswith('[') and alt.endswith(']') and len(alt) <= 20:
                emoji = alt[1:-1]
                if emoji not in SKIP_WORDS:
                    current_segment.append(emoji)
            elif alt and not any(skip in alt for skip in SKIP_WORDS):
                md_lines.append(('> ' if in_blockquery else '') + f'![{alt}]')
            continue

        link_match = re.match(r'- link(?:\s+"(.+?)")?.*?/url:\s*(.*)', stripped)
        if link_match:
            link_text, link_url = link_match.group(1) or '', link_match.group(2).strip().strip('"')
            if link_text and link_text not in SKIP_WORDS:
                current_segment.append(link_text.strip('"'))
            if in_blockquote and not reply_to_post_id:
                m = re.search(r'/\d+/(\d+)#comment', link_url)
                if m: reply_to_post_id = m.group(1)
            continue

        link_head_match = re.match(r'- link(?:\s+"(.+?)")?.*:$', stripped)
        if link_head_match:
            link_text = link_head_match.group(1) or ''
            if link_text and link_text not in SKIP_WORDS:
                current_segment.append(link_text.strip('"'))
            pending_link_check = True
            continue

        generic_match = re.match(r'- generic(?:\s+\[ref=e\d+\])?:\s*(.*)', stripped)
        if generic_match:
            text = generic_match.group(1).strip().strip('"')
            if text and text not in SKIP_WORDS and len(text) >= 1:
                current_segment.append(text)
            continue

        if re.match(r'- (?:list|listitem|table|row|cell)\b', stripped):
            flush_segment()
            continue

    flush_segment()
    result = '\n'.join(md_lines)
    result = re.sub(r'\n{3,}', '\n\n', result).strip()
    return result, reply_to_post_id, raw_time


# ════════════════════════════════════════
#  列表页帖子解析
# ════════════════════════════════════════

def parse_posts_from_snap(snap_file, author_id):
    """从列表页快照解析帖子基础信息"""
    with open(snap_file, encoding='utf-8', errors='replace') as f:
        content = f.read()
    posts = []
    blocks = re.split(r'(?=        - article \[ref=)', content)

    for block in blocks:
        if 'article [ref=' not in block:
            continue
        post_id_match = re.search(rf'/url: /{author_id}/(\d+)\n', block)
        if not post_id_match:
            continue
        post_id = post_id_match.group(1)
        post_url = f"https://xueqiu.com/{author_id}/{post_id}"

        time_match = re.search(r'link "([^"]*?·\s*来自[^"]+)" \[ref=', block)
        post_time = time_match.group(1) if time_match else ""

        heading_match = re.search(r'heading "([^"]+)" \[level=3\]', block)
        title = heading_match.group(1) if heading_match else ""

        comment_count = like_count = repost_count = 0
        read_count = ""
        for m in re.finditer(r'(?:link|text)[^"]*"·\s*讨论\s+(\d+)"?', block):
            comment_count = int(m.group(1))
        if not comment_count:
            for m in re.finditer(r'- text:\s*讨论\s+(\d+)', block):
                comment_count = int(m.group(1))
        for m in re.finditer(r'- text:\s*·\s*赞\s+(\d+)', block):
            like_count = int(m.group(1))
        if not like_count:
            for m in re.finditer(r'- text:\s*赞\s+(\d+)', block):
                like_count = int(m.group(1))

        repost_match = re.search(r'link "转发"', block)
        if repost_match:
            after = block[repost_match.end():repost_match.end()+300]
            rm = re.search(r'link "(\d+)"', after)
            if rm:
                repost_count = int(rm.group(1))

        read_match = re.search(
            r'- generic \[ref=[^\]]+\]:\s*阅读\s*\n\s*- generic \[ref=[^\]]+\]:\s*"?(\d[\d.,万千]*)"?',
            block
        )
        if not read_match:
            read_match = re.search(r'text:\s*阅读\s+([\d.,万千]+)', block)
        if read_match:
            read_count = read_match.group(1)

        SKIP = {'置顶','转发','收藏','设置','修改','删除','展开','查看对话','讨论','阅读','评论','分享'}
        raw_texts = re.findall(r'(?:^|\n)\s*- text: (.+)', block)
        clean = [t.strip().strip('"') for t in raw_texts if t.strip().strip('"') not in SKIP and not re.match(r'^\d+$', t.strip()) and len(t.strip()) > 1]

        posts.append({
            'post_id': post_id,
            'url': post_url,
            'time': post_time,
            'title': title,
            'snippet': ' '.join(clean[:8]),
            'comment_count': comment_count,
            'repost_count': repost_count,
            'like_count': like_count,
            'read_count': read_count,
        })

    return posts


# ════════════════════════════════════════
#  V4 规则分析引擎（内嵌，零外部依赖）
# ════════════════════════════════════════

# --- 股票关键词映射 ---
STOCK_MAP = {
    '腾讯': '00700.HK', '00700': '00700.HK',
    '唯品会': 'VIPS', 'VIPS': 'VIPS',
    '拼多多': 'PDD', 'PDD': 'PDD',
    '小赢': 'XYF', '小赢科技': 'XYF',
    '江南布衣': '03306.HK', 'JNBY': '03306.HK',
    '中化化肥': '00297.HK',
    '申洲国际': '02313.HK', '申洲': '02313.HK',
    '东江': '02283.HK', '东江集团': '02283.HK',
    '珩湾科技': '09609.HK', '珩湾': '09609.HK',
    '阿里': '09988.HK', '阿里巴巴': '09988.HK', 'BABA': '09988.HK',
    '美团': '03690.HK',
    '京东': '09618.HK', 'JD': '09618.HK',
    '百度': '09888.HK', 'BIDU': '09888.HK',
    '华晨中国': '01114.HK',
    '英美烟草': 'BTI',
    '比亚迪': '01211.HK', 'BYD': '01211.HK',
    '贵州茅台': '600519.SH', '茅台': '600519.SH',
    '招商银行': '03968.HK', '招行': '03968.HK',
    '中国平安': '02318.HK', '平安': '02318.HK',
    '网易': '09999.HK',
    '小米': '01810.HK',
    '快手': '01024.HK',
    '泡泡玛特': '09992.HK',
    '农夫山泉': '09633.HK',
    '格力': '000651.SZ',
    '宁德时代': '300750.SZ',
    '苹果': 'AAPL', 'Apple': 'AAPL',
    '英伟达': 'NVDA', 'NVIDIA': 'NVDA',
    '微软': 'MSFT',
    '特斯拉': 'TSLA',
}

CODE_TO_NAME = {}
for name, code in STOCK_MAP.items():
    if code not in CODE_TO_NAME or len(name) < len(CODE_TO_NAME[code]):
        CODE_TO_NAME[code] = name

OP_PATTERNS = {
    '买入': ['买入', '加仓', '买了', '买点', '建仓', '重仓', '补仓', '抄底', '进场'],
    '卖出': ['卖出', '减仓', '清仓', '止损', '卖了', '离场', '割肉', '止盈', '获利了结'],
    '持有': ['持仓', '继续持有', '不动', '长持', '继续拿', '躺平', '死拿', '装死'],
    '观察': ['观察', '关注', '研究', '考虑', '犹豫', '纠结', '等', '观望'],
}

POS_WORDS = ['看好', '乐观', '有信心', '很好', '不错', '增长', '回购', '分红',
             '上涨', '涨了', '牛', '超预期', '值得', '优秀', '低估', '便宜', '机会']

NEG_WORDS = ['担心', '亏损', '跌了', '下跌', '悲观', '风险', '止损', '不好', '错了',
             '熊', '大跌', '暴跌', '暴雷', '不及预期', '高位', '泡沫', '套牢', '割肉']

TOPIC_PATTERNS = {
    '估值分析': ['估值', 'PE', 'PB', 'DCF', '市盈率', '市净率', 'EPS', 'PS'],
    '财务分析': ['营收', '利润', '财报', '年报', '季报', '毛利率', '净利率', 'ROE', 'ROA'],
    '股东回报': ['回购', '分红', '股息', '派息'],
    '业绩分析': ['业绩', '增长', '下滑', '收入', '盈利', '同比', '环比'],
    '公司研究': ['调研', '产品', '管理层', '竞争对手', '壁垒', '商业模式', '护城河', '核心竞争力'],
    '行业分析': ['行业', '竞争', '市场份额', '赛道', '趋势', '格局', '龙头'],
    '宏观经济': ['经济', 'GDP', '通胀', '利率', '货币', '政策', '美联储', '央行', '降息', '加息'],
    '市场情绪': ['情绪', '恐慌', '贪婪', '散户', '机构', '换手', '量能'],
    '投资理念': ['价值投资', '长期持有', '复利', '巴菲特', '芒格', '费雪', '唐朝', '烟蒂', '安全边际', '能力圈'],
    '操作记录': ['买入', '卖出', '加仓', '减仓', '止损', '清仓', '建仓', '调仓', '仓位'],
    '港股': ['港股', '恒生', 'H股', '香港'],
    '美股': ['美股', '纳斯达克', '标普'],
    'A股': ['A股', '沪深', '创业板', '科创板'],
    '科技互联网': ['人工智能', '云计算', '芯片', '半导体', 'SaaS', '自动驾驶', '大模型', 'ChatGPT'],
    '消费': ['消费', '零售', '品牌', '服装', '食品', '白酒'],
    '金融': ['银行', '保险', '券商', '贷款'],
    '新能源': ['新能源', '光伏', '风电', '锂电', '储能', '电动车'],
    '医药': ['医药', '创新药', 'CXO', '医疗器械'],
    '读书笔记': ['读书', '笔记', '书', '学习', '总结'],
    '生活感悟': ['生活', '感悟', '心态', '随笔', '日记'],
    'ETF基金': ['ETF', '基金', '指数基金', 'LOF', '定投'],
}


def classify_post_type(full_content):
    """识别帖子类型：original / reply / error / empty"""
    if not full_content or not full_content.strip():
        return {'post_type': 'empty', 'own_text': '', 'quote_text': ''}
    text = full_content.strip()

    if '当前网址:' in text[:50] or '请求时间:' in text[:50]:
        return {'post_type': 'error', 'own_text': '', 'quote_text': ''}

    # 格式C：Markdown blockquote (> **引用：**)
    if '> **引用：**' in text:
        lines = text.split('\n')
        own_parts, quote_parts = [], []
        in_quote = False
        for line in lines:
            stripped = line.strip()
            if not stripped:
                if in_quote: quote_parts.append('')
                else: own_parts.append('')
                continue
            if stripped == '> **引用：**':
                in_quote = True; continue
            if in_quote and stripped.startswith('> '):
                quote_parts.append(stripped[2:].strip()); continue
            if in_quote and stripped == '>':
                continue
            if in_quote and not stripped.startswith('>'):
                in_quote = False; own_parts.append(stripped); continue
            if not in_quote:
                own_parts.append(stripped)
        own_text, quote_text = '\n'.join(own_parts).strip(), '\n'.join(quote_parts).strip()
        if quote_text:
            return {'post_type': 'reply', 'own_text': own_text, 'quote_text': quote_text}

    # 格式A：// 分隔
    quote_match = re.search(r'^(.*?)//(.*?)$', text, re.DOTALL)
    if quote_match:
        before, after = quote_match.group(1).strip(), quote_match.group(2).strip()
        if before.startswith(':') and ':回复' in after and len(before) < 500:
            quote_text = before[1:].strip()
            return {'post_type': 'reply', 'own_text': _extract_own_reply(after), 'quote_text': quote_text}

    # 格式B："作者" 标签
    if '\n作者\n' in text:
        lines = text.split('\n')
        ai_list = [i for i, l in enumerate(lines) if l.strip() == '作者']
        if ai_list:
            own_parts, quote_parts = [], []
            i = 0; in_q = False
            while i < len(lines):
                line = lines[i].strip()
                if not line or line in {'讨论', '赞', '好友'} or re.match(r'^\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}$', line):
                    i += 1; continue
                if line == '作者' and i+1 < len(lines) and lines[i+1].strip() not in {'讨论', '赞', '好友'}:
                    in_q = True; qname = lines[i+1].strip(); i += 2
                    if i < len(lines) and lines[i].strip().startswith('：'):
                        qc = []
                        while i < len(lines) and lines[i].strip().startswith('：'):
                            qc.append(lines[i].strip()[1:].strip()); i += 1
                        quote_parts.append(qname + ': ' + ' '.join(qc))
                    else:
                        quote_parts.append(qname)
                    continue
                if line.startswith('：') and not in_q:
                    in_q = True; quote_parts.append(line[1:].strip()); i += 1
                    while i < len(lines) and lines[i].strip().startswith('：'):
                        quote_parts.append(lines[i].strip()[1:].strip()); i += 1
                    continue
                if in_q: in_q = False
                own_parts.append(line); i += 1
            qt, ot = '\n'.join(quote_parts).strip(), '\n'.join(own_parts).strip()
            if qt:
                return {'post_type': 'reply', 'own_text': ot, 'quote_text': qt}

    return {'post_type': 'original', 'own_text': text, 'quote_text': ''}


def _extract_own_reply(reply_section):
    """从对话链中提取用户自己的话"""
    lines = reply_section.split('\n'); own = []
    started = False
    for line in lines:
        if line.strip() == ':回复': started = True; continue
        if not started: continue
        s = line.strip()
        if not s or s in {'讨论', '赞', '好友'}: continue
        if s.startswith('：'): continue
        if s == '好友': continue
        if s.startswith(':'): own.append(s[1:].strip())
        elif s not in {'©', 'XUEQIU.COM'}: own.append(s)
    return '\n'.join(own).strip()


def analyze_post(title, full_content, category):
    """对单条帖子做完整 V4 规则分析"""
    content = (full_content or '').strip()
    type_info = classify_post_type(content)
    post_type, own_text = type_info['post_type'], type_info['own_text']
    analysis_text = own_text if (post_type == 'reply' and own_text) else content
    text = analysis_text + ' ' + (title or '')

    # 提取股票
    stocks = []
    seen_stocks = set()
    for name, code in STOCK_MAP.items():
        if name in text and code not in seen_stocks:
            seen_stocks.add(code)
            stocks.append({'code': code, 'name': CODE_TO_NAME.get(code, code)})

    # 操作意图
    ops = []
    for op_type, kws in OP_PATTERNS.items():
        if any(kw in text for kw in kws): ops.append(op_type)

    # 情感
    pos_c = sum(1 for w in POS_WORDS if w in text)
    neg_c = sum(1 for w in NEG_WORDS if w in text)
    sentiment = '看多' if pos_c > neg_c + 1 else ('看空' if neg_c > pos_c + 1 else '中性')

    # 主题标签
    topics, topics_seen = [], set()
    for topic, kws in TOPIC_PATTERNS.items():
        if topic not in topics_seen and any(kw in text for kw in kws):
            topics.append(topic); topics_seen.add(topic)

    # 内容类型
    cl = len(analysis_text)
    if cl < 10: ct = '空内容'
    elif re.search(r'(买入|卖出|加仓|减仓|建仓|清仓).{0,20}(元|股|手|均价|成本)', text): ct = '交易记录'
    elif re.search(r'\d+\.?\d*\s*(亿|万|%)', text) and len(re.findall(r'\d+\.?\d*\s*(亿|万|%)', text)) >= 3: ct = '数据分析'
    elif re.search(r'(觉得|认为|看法|观点|怎么)', text): ct = '讨论交流'
    elif category in ('读书笔记',) or re.search(r'(读书|笔记|读后)', text): ct = '读书笔记'
    elif cl < 80: ct = '短评'
    elif cl > 500: ct = '深度分析'
    else: ct = '一般讨论'

    # 投资相关性
    trade_intent = ops[0] if ops else '无'
    if cl < 5: ir = 'none'
    elif stocks and trade_intent != '无' and cl > 100: ir = 'high'
    elif stocks and ct in ('深度分析', '数据分析', '交易记录') and cl > 100: ir = 'high'
    elif len(stocks) >= 2 and cl > 100: ir = 'high'
    elif stocks and cl > 200 and category not in ('读书笔记', '生活随笔'): ir = 'high'
    elif stocks and cl > 50: ir = 'medium'
    elif stocks and cl > 10: ir = 'low'
    elif stocks: ir = 'low'
    elif category in CATEGORY_KEYWORDS and category not in ('读书笔记', '生活随笔'): ir = 'medium'
    elif ct in ('交易记录', '数据分析', '深度分析'): ir = 'medium'
    elif trade_intent != '无': ir = 'low'
    elif category in ('读书笔记', '生活随笔'): ir = 'none'
    else: ir = 'none'

    # 质量评分
    depth = '短评' if cl < 80 else ('中篇' if cl < 300 else ('长文' if cl < 800 else '深度长文'))
    if post_type in ('error', 'empty') or cl < 10: qs = 0
    elif ir == 'none': qs = 1
    else:
        qs = 2
        if stocks: qs += 1
        if depth in ('长文', '深度长文'): qs += 1
        if ops: qs += 1
        if ct in ('深度分析', '数据分析', '交易记录'): qs += 1
        if ir == 'high': qs += 1
        qs = min(qs, 5)

    # 摘要
    summary = analysis_text
    summary = re.sub(r'//\s*@[^\n]+', '', summary)
    summary = re.sub(r'@\w+\s*[:：]?\s*', '', summary)
    summary = re.sub(r'https?://[^\s]+', '', summary)
    for pat in [r'修改于', r'发布于', r'来自\w+', r'讨论\s*\d+', r'赞\s*\d+']:
        summary = re.sub(pat, '', summary)
    summary = re.sub(r'\n{3,}', '\n\n', summary).strip()[:300]

    stock_names = [s['name'] for s in stocks]

    return {
        'post_type': post_type,
        'own_text': own_text or None,
        'quote_text': type_info.get('quote_text') or None,
        'tags': json.dumps(stock_names, ensure_ascii=False) if stock_names else None,
        'sentiment': sentiment,
        'trade_intent': trade_intent,
        'content_type': ct,
        'quality_score': qs,
        'investment_relevance': ir,
        'word_count': cl,
        'summary': summary or None,
        'content_depth': depth,
        'topics': json.dumps(topics, ensure_ascii=False) if topics else None,
    }


def classify_post(title, content):
    """按关键词分类帖子"""
    text = (title + ' ' + content).lower()
    best_cat, best_score = FALLBACK_CATEGORY, 0
    for cat, keywords in CATEGORY_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw.lower() in text)
        if score > best_score:
            best_score = score; best_cat = cat
    return best_cat


# ════════════════════════════════════════
#  数据库操作
# ════════════════════════════════════════

def init_database(db_path):
    """初始化数据库，创建 xueqiu_posts 表"""
    conn = sqlite3.connect(db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS xueqiu_posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id TEXT UNIQUE NOT NULL,
            stock_code TEXT,
            source TEXT DEFAULT 'xueqiu',
            title TEXT,
            content TEXT,
            full_content TEXT,
            author TEXT,
            author_id TEXT,
            url TEXT,
            published_at TEXT,
            crawled_at TEXT,
            category TEXT,
            like_count INTEGER DEFAULT 0,
            comment_count INTEGER DEFAULT 0,
            repost_count INTEGER DEFAULT 0,
            read_count TEXT,
            image_ocr_text TEXT,
            post_type TEXT DEFAULT 'original',
            own_text TEXT,
            quote_text TEXT,
            investment_relevance TEXT,
            sentiment TEXT,
            trade_intent TEXT,
            content_type TEXT,
            quality_score INTEGER DEFAULT 0,
            word_count INTEGER DEFAULT 0,
            summary TEXT,
            content_depth TEXT,
            topics TEXT,
            tags TEXT,
            reply_to_post_id TEXT
        )
    """)
    conn.commit()
    return conn


def get_posts_needing_full(conn, author, force=False, limit=0, latest=False):
    """返回需要采集正文的帖子列表"""
    order = "id DESC" if latest else "id ASC"
    if force:
        rows = conn.execute(
            f"SELECT post_id, url, title, content FROM xueqiu_posts WHERE author=? ORDER BY {order}",
            (author,)
        ).fetchall()
    else:
        rows = conn.execute(
            f"""SELECT post_id, url, title, content FROM xueqiu_posts
                WHERE author=? AND (full_content IS NULL OR full_content='')
                ORDER BY {order}""",
            (author,)
        ).fetchall()
    if limit > 0:
        rows = rows[:limit]
    return [{'post_id': r[0], 'url': r[1], 'title': r[2], 'snippet': r[3]} for r in rows]


def get_existing_ids(conn, author):
    return {r[0] for r in conn.execute("SELECT post_id FROM xueqiu_posts WHERE author=?", (author,)).fetchall() if r[0]}


def upsert_post_basic(conn, p, author, author_id):
    """插入或更新帖子基础信息"""
    pub_date = parse_xueqiu_time(p.get('time', ''))
    conn.execute(
        """INSERT OR IGNORE INTO xueqiu_posts
           (post_id, source, title, content, author, author_id, url, published_at, crawled_at,
            like_count, comment_count, repost_count, read_count)
           VALUES (?, 'xueqiu', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (p['post_id'], p.get('title', ''), p.get('snippet', ''),
         author, author_id, p['url'], pub_date,
         datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
         p.get('like_count', 0), p.get('comment_count', 0),
         p.get('repost_count', 0), p.get('read_count', ''))
    )
    conn.commit()


def update_interaction_data(conn, p):
    """更新已有帖子的互动数据"""
    vals = (p.get('like_count', 0), p.get('comment_count', 0),
            p.get('repost_count', 0), p.get('read_count', ''), p['post_id'])
    if any(vals[:-1]):
        conn.execute(
            """UPDATE xueqiu_posts SET
               like_count=CASE WHEN ?>0 THEN ? ELSE like_count END,
               comment_count=CASE WHEN ?>0 THEN ? ELSE comment_count END,
               repost_count=CASE WHEN ?>0 THEN ? ELSE repost_count END,
               read_count=CASE WHEN ?!='' THEN ? ELSE read_count END
               WHERE post_id=?""",
            vals
        )
        conn.commit()


def update_full_content(conn, post_id, full_content, category, title='', reply_to_post_id='', raw_time=''):
    """更新正文 + 自动做 V4 分析"""
    try:
        result = analyze_post(title, full_content, category)
        pt, ir, qs, wc = result['post_type'], result['investment_relevance'], result['quality_score'], result['word_count']

        pub_date = ""
        raw_db = conn.execute("SELECT published_at FROM xueqiu_posts WHERE post_id=?", (post_id,)).fetchone()
        if raw_db and raw_db[0]:
            parsed = parse_xueqiu_time(raw_db[0])
            if parsed != raw_db[0]: pub_date = parsed
        elif raw_time:
            parsed = parse_xueqiu_time(raw_time)
            if parsed: pub_date = parsed

        fields = [
            'full_content=?, category=?, crawled_at=?',
            'post_type=?', 'own_text=?', 'quote_text=?',
            'sentiment=?', 'trade_intent=?', 'content_type=?',
            'quality_score=?', 'investment_relevance=?', 'word_count=?',
            'summary=?', 'content_depth=?', 'topics=?', 'tags=?',
        ]
        params = [full_content, category, datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                  result['post_type'], result.get('own_text'), result.get('quote_text'),
                  result['sentiment'], result['trade_intent'], result['content_type'],
                  result['quality_score'], result['investment_relevance'], result['word_count'],
                  result['summary'], result['content_depth'], result['topics'], result['tags']]

        if pub_date:
            fields.append('published_at=?'); params.append(pub_date)

        fields.append('reply_to_post_id=CASE WHEN ? IS NOT NULL AND ?!='' THEN ? ELSE reply_to_post_id END')
        params.extend([reply_to_post_id, reply_to_post_id, reply_to_post_id])

        fields.append('WHERE post_id=?')
        params.append(post_id)

        sql = "UPDATE xueqiu_posts SET " + ", ".join(fields)
        conn.execute(sql, params)
        conn.commit()
        return pt, ir, qs, wc
    except Exception as e:
        print(f'  [分析失败] post_id={post_id}: {e}')
        conn.execute("UPDATE xueqiu_posts SET full_content=?, category=?, crawled_at=? WHERE post_id=?",
                     (full_content, category, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), post_id))
        conn.commit()
        return '?', '?', 0, 0


def batch_analyze(conn, only_missing=False):
    """批量 V4 分析未分析的帖子"""
    where = " AND (post_type IS NULL OR post_type='')" if only_missing else ""
    rows = conn.execute(
        f"""SELECT post_id, title, full_content, category FROM xueqiu_posts
            WHERE full_content IS NOT NULL AND full_content!=''{where}
            ORDER BY id"""
    ).fetchall()
    processed = skipped = 0
    for row in rows:
        pid, title, fc, cat = row
        if len(fc or '') < 10: skipped += 1; continue
        result = analyze_post(title, fc, cat)
        conn.execute(
            """UPDATE xueqiu_posts SET
               post_type=?, own_text=?, quote_text=?, tags=?, sentiment=?,
               trade_intent=?, content_type=?, quality_score=?, investment_relevance=?,
               word_count=?, summary=?, content_depth=?, topics=?
               WHERE post_id=?""",
            (result['post_type'], result.get('own_text'), result.get('quote_text'), result['tags'],
             result['sentiment'], result['trade_intent'], result['content_type'],
             result['quality_score'], result['investment_relevance'], result['word_count'],
             result['summary'], result['content_depth'], result['topics'], pid)
        )
        processed += 1
    conn.commit()
    return processed, skipped


# ════════════════════════════════════════
#  阶段一：采集帖子列表
# ════════════════════════════════════════

def phase1_collect_list(cfg, author, author_id, home_url, existing_ids, conn, stop_on_no_new=3):
    print(f"\n{'─'*50}\n  阶段一：采集帖子列表（反爬虫模式）\n  [停止策略] 连续 {stop_on_no_new} 页无新帖停止\n{'─'*50}")

    run_cmd(cfg, ["goto", home_url], retries=MAX_RETRIES)
    time.sleep(random.uniform(3, 5))

    all_discovered, new_basic = [], 0
    page_num, max_pages, err_streak = 1, 200, 0
    consecutive_empty = consecutive_no_new = 0

    while page_num <= max_pages:
        print(f"  [{datetime.now().strftime('%H:%M:%S')}] 列表第 {page_num} 页", end=" ... ")
        if page_num > 1:
            time.sleep(random.uniform(REQUEST_INTERVAL, REQUEST_INTERVAL + 2))

        snap = take_snapshot(cfg)
        if not snap:
            print("❌ 快照失败")
            err_streak += 1
            if err_streak >= 3: break
            time.sleep(ERROR_DELAY); continue

        err_streak = 0
        posts = parse_posts_from_snap(snap, author_id)

        if len(posts) == 0:
            consecutive_empty += 1
            if consecutive_empty >= 3:
                print("\n  连续3页无数据，到达末尾。"); break
            print(f"⚠️  无数据 ({consecutive_empty}/3)")
        else:
            consecutive_empty = 0; page_new = 0
            for p in posts:
                if p['post_id'] not in existing_ids:
                    upsert_post_basic(conn, p, author, author_id)
                    existing_ids.add(p['post_id']); new_basic += 1; page_new += 1
                else:
                    update_interaction_data(conn, p)
                all_discovered.append(p)

            if page_new == 0:
                consecutive_no_new += 1
                print(f"✅ {len(posts)}条，全部已有 ({consecutive_no_new}/{stop_on_no_new})")
                if consecutive_no_new >= stop_on_no_new:
                    print(f"\n  连续{stop_on_no_new}页无新帖，停止扫描。"); break
            else:
                consecutive_no_new = 0
                print(f"✅ {len(posts)}条，新增{page_new}条（累计{new_basic}）")

        next_ref = find_next_page_ref(snap)
        if not next_ref:
            print("\n  已到最后一页。"); break

        run_cmd(cfg, ["click", next_ref], timeout=20, retries=MAX_RETRIES)
        time.sleep(random.uniform(2, 4)); page_num += 1
        if page_num % 10 == 0:
            d = random.uniform(5, 8)
            print(f"    [休息] {page_num}页后休息 {d:.1f}s..."); time.sleep(d)

    print(f"\n  列表完成：发现 {len(all_discovered)} 条，新增 {new_basic} 条")
    return all_discovered


# ════════════════════════════════════════
#  阶段二：采集完整正文
# ════════════════════════════════════════

def phase2_collect_full(cfg, posts_needing_full, conn, author_dir):
    total = len(posts_needing_full)
    print(f"\n{'─'*50}\n  阶段二：采集完整正文（共 {total} 条）\n{'─'*50}")
    if total == 0:
        print("  所有帖子已有正文，跳过。"); return 0

    success, fail_ids = 0, []
    for i, p in enumerate(posts_needing_full, 1):
        pid, purl, title = p['post_id'], p['url'], p.get('title', '')
        print(f"  [{i}/{total}] {pid}", end=" ... ")
        if i > 1: time.sleep(random.uniform(MIN_DELAY, MAX_DELAY))

        for retry in range(MAX_RETRIES):
            try:
                run_cmd(cfg, ["goto", purl], timeout=25, retries=0)
                out, err = run_cmd(cfg, ["snapshot"], timeout=30)
                if "429" in err:
                    if retry < MAX_RETRIES - 1:
                        backoff = ERROR_DELAY * (2**retry)
                        print(f"[限流] 休息 {backoff:.1f}s...", end=" ")
                        time.sleep(backoff); continue
                    else: print("❌ 限流"); fail_ids.append(pid); break

                time.sleep(random.uniform(2, 4))
                snap = take_snapshot(cfg)
                if not snap:
                    if retry < MAX_RETRIES - 1: print(f"[重试{retry+1}]", end=" "); time.sleep(2); continue
                    print("❌ 快照失败"); fail_ids.append(pid); break

                fc, reply_id, raw_t = extract_full_content_from_snap(snap)
                if not fc or len(fc) < 5:
                    if retry < MAX_RETRIES - 1: print(f"[重试{retry+1}]", end=" "); time.sleep(2); continue
                    print("⚠️  正文空"); fail_ids.append(pid); break

                # 滚动加载图片
                for _ in range(3):
                    run_cmd(cfg, ["eval", "() => { window.scrollTo(0, document.body.scrollHeight); }"], timeout=10, no_delay=True)
                    time.sleep(0.3)
                run_cmd(cfg, ["eval", "() => { window.scrollTo(0, 0); }"], timeout=10, no_delay=True)
                time.sleep(0.3)

                # 图片处理
                images_dir = os.path.join(author_dir, "images")
                img_list = extract_images_from_page(cfg)
                img_cnt, ocr_txt = 0, ""
                if img_list:
                    dl = download_images(img_list, pid, images_dir)
                    img_cnt = sum(1 for r in dl if r.get('success'))
                    if img_cnt > 0:
                        fc = update_images_in_markdown(fc, dl)
                        ocr_txt = ocr_post_images(pid, images_dir)
                        if ocr_txt:
                            conn.execute("UPDATE xueqiu_posts SET image_ocr_text=? WHERE post_id=?", (ocr_txt, pid))
                            conn.commit()

                cat = classify_post(title, fc)
                pt, ir, qs, wc = update_full_content(conn, pid, fc, cat, title, reply_to_post_id=reply_id, raw_time=raw_t)
                success += 1
                icons = {'original':'📝','reply':'💬','error':'⚠️','empty':'📭'}
                ri = f"→#{reply_id}" if reply_id else ""
                ii = f"|🖼️{img_cnt}张" if img_cnt > 0 else ""
                oi = f"(OCR:{len(ocr_txt)}字)" if ocr_txt else ""
                print(f"✅ [{cat}] {icons.get(pt,'❓')}{pt}{ri}|{wc}字|相关:{ir}|质量:{qs}{ii}{oi}")

                if success % 10 == 0:
                    save_json_backup(conn, author_dir)
                    print(f"    [备份] {success}条")
                if success % 20 == 0:
                    rt = random.uniform(8, 12)
                    print(f"    [休息] {success}条后休息{rt:.1f}s..."); time.sleep(rt)
                break

            except subprocess.TimeoutExpired:
                if retry < MAX_RETRIES - 1: print(f"[超时{retry+1}]", end=" "); time.sleep(3); continue
                print("❌ 超时"); fail_ids.append(pid); break
            except Exception as e:
                if retry < MAX_RETRIES - 1: print(f"[异常{retry+1}] {e}", end=" "); time.sleep(2); continue
                print(f"❌ {e}"); fail_ids.append(pid); time.sleep(2); break

    print(f"\n  正文完成：成功 {success} 条，失败 {len(fail_ids)} 条")
    if fail_ids: print(f"  失败ID：{fail_ids[:20]}{'...' if len(fail_ids)>20 else ''}")
    return success


# ════════════════════════════════════════
#  阶段三：导出 JSON + MD
# ════════════════════════════════════════

def _post_to_md(post):
    """单条帖子转 Markdown"""
    title = post.get('title') or '（无标题）'
    lines = [f"## {title}\n", f"- **链接**：{post.get('url', '')}",
             f"- **时间**：{post.get('published_at', '')}", f"- **分类**：{post.get('category', '')}"]
    if post.get('read_count'): lines.append(f"- **阅读数**：{post.get('read_count', '')}")
    stats = []
    if post.get('like_count'): stats.append(f"👍 {post['like_count']}")
    if post.get('comment_count'): stats.append(f"💬 {post['comment_count']}")
    if post.get('repost_count'): stats.append(f"🔁 {post['repost_count']}")
    if stats: lines.append(f"- **互动**：{'  '.join(stats)}")
    lines.append("")
    lines.append(post.get('full_content') or post.get('snippet') or '')
    ocr = post.get('image_ocr_text', '')
    if ocr: lines.append(f"\n> 📷 **图片识别内容**：\n> {ocr.replace(chr(10), chr(10)+'> ')}")
    lines.append("\n---\n")
    return '\n'.join(lines)


def save_json_backup(conn, author_dir):
    """导出 JSON + Markdown 备份"""
    rows = conn.execute(
        """SELECT post_id,url,title,content,full_content,category,published_at,read_count,
                  like_count,comment_count,repost_count,image_ocr_text
           FROM xueqiu_posts WHERE full_content IS NOT NULL AND full_content!=''
           ORDER BY published_at DESC"""
    ).fetchall()

    all_posts, by_category = [], {}
    for r in rows:
        post = dict(zip(['post_id','url','title','snippet','full_content','category',
                         'published_at','read_count','like_count','comment_count',
                         'repost_count','image_ocr_text'], r))
        all_posts.append(post)
        cat = r[5] or FALLBACK_CATEGORY
        by_category.setdefault(cat, []).append(post)

    os.makedirs(author_dir, exist_ok=True)
    with open(os.path.join(author_dir, "posts_full.json"), 'w', encoding='utf-8') as f:
        json.dump(all_posts, f, ensure_ascii=False, indent=2)

    classified_dir = os.path.join(author_dir, "classified"); os.makedirs(classified_dir, exist_ok=True)
    for cat, posts in by_category.items():
        safe = re.sub(r'[\\/:*?"<>|]', '_', cat)
        with open(os.path.join(classified_dir, f"{safe}.json"), 'w', encoding='utf-8') as f:
            json.dump(posts, f, ensure_ascii=False, indent=2)

    md_dir = os.path.join(author_dir, "md"); os.makedirs(md_dir, exist_ok=True)
    author_name = os.path.basename(author_dir)
    with open(os.path.join(author_dir, "posts_full.md"), 'w', encoding='utf-8') as f:
        f.write(f"# {author_name} 雪球帖子全集\n\n> 共{len(all_posts)}条，生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n---\n\n")
        for post in all_posts: f.write(_post_to_md(post))

    for cat, posts in by_category.items():
        safe = re.sub(r'[\\/:*?"<>|]', '_', cat)
        with open(os.path.join(md_dir, f"{safe}.md"), 'w', encoding='utf-8') as f:
            f.write(f"# {cat}（{len(posts)}篇）\n\n---\n\n")
            for post in posts: f.write(_post_to_md(post))

    return len(all_posts), by_category


# ════════════════════════════════════════
#  主流程
# ════════════════════════════════════════

def main():
    args = parse_args()
    cfg = resolve_config(args)

    # 设置日志双写
    os.makedirs(cfg['snap_dir'], exist_ok=True)
    sys.stdout = _Tee(sys.stdout, cfg['log_path'])

    print(f"\n{'═'*60}\n  🧊 雪球帖子采集系统 v1.0（通用 Skill 版）\n  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n{'═'*60}")

    # 从 URL 提取 author_id
    m = re.search(r'/u/(\d+)', args.url)
    if not m:
        print("❌ 无法从 URL 提取用户 ID，格式：https://xueqiu.com/u/XXXXXX")
        sys.exit(1)
    author_id = m.group(1)
    author = args.author
    print(f"  发帖人：{author} | ID：{author_id}")

    # 准备目录
    author_dir = os.path.join(cfg['out_root'], author)
    os.makedirs(author_dir, exist_ok=True)
    print(f"  数据库：{cfg['db_path']}")
    print(f"  输出目录：{author_dir}")

    # 初始化/连接数据库
    conn = init_database(cfg['db_path'])

    # 查询状态
    existing_ids = get_existing_ids(conn, author)
    posts_needing = get_posts_needing_full(conn, author, force=args.force_collect,
                                           limit=args.limit, latest=args.latest)

    print(f"\n  本地数据：已有 {len(existing_ids)} 条")
    if args.force_collect:
        mode = f"强制重采（{args.limit}条" + ("" if not args.limit else "）")
        if args.latest: mode += " 最新优先"
        print(f"  📌 {mode}")
    else:
        print(f"  待补全正文：{len(posts_needing)} 条")

    # 决定策略
    if args.force_collect:
        do_list = False; print(f"\n  [强制] 跳过列表，直接重采正文")
    elif len(existing_ids) == 0:
        do_list = True; print(f"\n  [新] 全量采集（列表+正文）")
    elif len(posts_needing) > 0 and not args.refresh_list:
        do_list = False; print(f"\n  [增量] 补全正文（加 --refresh-list 可扫新帖）")
    else:
        do_list = True; print(f"\n  [刷新] 扫描列表找新帖...")

    # 启动浏览器
    print(f"\n  检查浏览器...")
    ensure_browser_open(cfg, args.url)

    # 阶段一
    if do_list:
        phase1_collect_list(cfg, author, author_id, args.url, existing_ids, conn,
                            stop_on_no_new=args.stop_on_no_new)

    # 重新获取待补全列表
    posts_needing = get_posts_needing_full(conn, author, force=args.force_collect,
                                           limit=args.limit, latest=args.latest)
    print(f"\n  待采正文：{len(posts_needing)} 条")

    # 阶段二
    success = phase2_collect_full(cfg, posts_needing, conn, author_dir)

    # 阶段三：导出
    print(f"\n{'─'*50}\n  阶段三：导出 JSON + MD\n{'─'*50}")
    total_saved, by_cat = save_json_backup(conn, author_dir)
    print(f"  全量 JSON：{os.path.join(author_dir, 'posts_full.json')}（{total_saved}条）")
    print(f"  全量 MD ：{os.path.join(author_dir, 'posts_full.md')}（{total_saved}条）")
    print(f"  分类（{len(by_cat)}个）：")
    for cat, posts in sorted(by_cat.items(), key=lambda x:-len(x[1])):
        print(f"    [{cat}] {len(posts)}条")

    # 阶段四：V4 回填
    print(f"\n{'─'*50}\n  阶段四：V4 规则分析回填\n{'─'*50}")
    try:
        missing = conn.execute("""SELECT COUNT(*) FROM xueqiu_posts
            WHERE full_content IS NOT NULL AND full_content!='' AND (post_type IS NULL OR post_type='')""").fetchone()[0]
        if missing > 0:
            print(f"  {missing} 条缺少分析，执行回填...")
            proc, skip = batch_analyze(conn, only_missing=True)
            print(f"  ✅ 回填完成：处理{proc}条，跳过{skip}条")
        else:
            print(f"  ✅ 所有帖子已有V4分析")
    except Exception as e:
        print(f"  ⚠️ V4分析出错: {e}")

    # 统计汇总
    print(f"\n{'─'*50}\n  📊 统计汇总\n{'─'*50}")
    stats = conn.execute("""SELECT post_type, investment_relevance, COUNT(*)
        FROM xueqiu_posts WHERE full_content IS NOT NULL AND full_content!=''
        GROUP BY post_type, investment_relevance ORDER BY post_type, investment_relevance""").fetchall()
    print(f"  {'类型':<10s} {'相关性':<8s} {'数量':>6s}\n  {'-'*28}")
    for pt, ir, cnt in stats: print(f"  {pt:<10s} {ir:<8s} {cnt:>6d}")

    conn.close()

    # 最终报告
    img_total = len([f for f in os.listdir(os.path.join(author_dir, "images")) if not f.startswith('.')]) \
                 if os.path.isdir(os.path.join(author_dir, "images")) else 0
    print(f"\n{'═'*60}\n  ✅ 采集完成！\n  本次补全：{success}条 | 图片：{img_total}张\n  数据目录：{author_dir}\n{'═'*60}")


if __name__ == "__main__":
    main()
