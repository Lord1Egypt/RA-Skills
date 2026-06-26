# -*- coding: utf-8 -*-
"""
纯 HTTP 版批量抓取：无需浏览器，直接请求微信文章 URL
生成 Markdown 文件（PDF 需手动用浏览器打印）

适合：大量文章快速离线存档（文字内容）
注意：部分微信文章有反爬限制，此时请使用 batch_scrape.py（需浏览器）

用法：
  python3 scripts/batch_http.py [xlsx路径]
  # xlsx 列要求：col[1]=标题，col[2]=日期，col[5]=URL
"""
import sys, os, re, time, base64
from datetime import date

OUT_DIR = os.path.expanduser(f'~/Desktop/{date.today().strftime("%Y-%m-%d")}')
os.makedirs(OUT_DIR, exist_ok=True)

# ════════════════════════════════════════════════════════
# 依赖
# ════════════════════════════════════════════════════════
import importlib.util
REQUIRED = ['requests', 'openpyxl']
missing = [p for p in REQUIRED if importlib.util.find_spec(p) is None]
if missing:
    print(f"❌ 缺少依赖: {', '.join(missing)}")
    print(f"   请先安装: pip install {' '.join(missing)}")
    sys.exit(1)

import openpyxl

# ════════════════════════════════════════════════════════
# 辅助
# ════════════════════════════════════════════════════════
def sanitize(name):
    name = str(name).strip()
    name = re.sub(r'[\\/:*?"<>|]', '', name)
    name = re.sub(r'\s+', ' ', name)
    return name[:80]

def parse_date(s):
    if not s:
        return 'unknown'
    s = str(s)
    for pat in [r'(\d{4})[-/年](\d{1,2})[-/月](\d{1,2})',
                r'(\d{4})(\d{2})(\d{2})']:
        m = re.search(pat, s)
        if m:
            return f"{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"
    return 'unknown'

def fetch_wx_article(url):
    """
    使用 requests 抓取微信文章内容（绕过部分反爬），
    提取标题、日期、正文段落和图片。
    """
    import requests
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Referer': 'https://mp.weixin.qq.com/',
    }
    try:
        r = requests.get(url, headers=headers, timeout=20, allow_redirects=True)
        r.encoding = 'utf-8'
        html = r.text
    except Exception as e:
        return None, str(e)

    from html.parser import HTMLParser

    class WxParser(HTMLParser):
        def __init__(self):
            super().__init__()
            self.title = ''
            self.author = ''
            self.pub_date = ''
            self.body_paras = []
            self.images = []
            self.in_title = False
            self.in_content = False
            self.in_js_name = False
            self.current_tag = ''
            self.in_section = False

        def handle_starttag(self, tag, attrs):
            self.current_tag = tag
            attrs_dict = dict(attrs)

            if tag in ('h1', 'h2', 'h3'):
                self.in_title = True

            if attrs_dict.get('id') == 'js_content':
                self.in_content = True
            if attrs_dict.get('id') == 'js_name':
                self.in_js_name = True

            if tag == 'img':
                # 优先 data-src（懒加载），次取 data-wap_src，再取 src
                src = (attrs_dict.get('data-src') or
                       attrs_dict.get('data-wap_src') or
                       attrs_dict.get('src') or '')
                if src and ('mmbiz' in src or src.startswith('http')):
                    if src.startswith('//'):
                        src = 'https:' + src
                    if src not in self.images:
                        self.images.append(src)

        def handle_data(self, data):
            data = data.strip()
            if not data:
                return
            if self.in_title and not self.title:
                self.title = data
                self.in_title = False
            if self.in_js_name and not self.author:
                self.author = data
                self.in_js_name = False
            if self.in_content and self.current_tag == 'p':
                # 过滤微信运营内容
                skip_patterns = (
                    '阅读', '点赞', '在看', '分享', '收藏', '赞赏',
                    '长按', '扫码', '识别', '二维码',
                    '发表于', '来源', '更多', '往期', '相关', '热门',
                )
                if not any(data.startswith(p) for p in skip_patterns):
                    if len(data) > 3:
                        self.body_paras.append(data)

        def handle_endtag(self, tag):
            if tag in ('p', 'section'):
                self.in_section = False

    parser = WxParser()
    try:
        parser.feed(html)
    except Exception:
        pass

    # 备选：从 <title> 提取
    if not parser.title:
        m = re.search(r'<title>([^<]+)</title>', html)
        if m:
            t = m.group(1).replace(' - 复旦大学附属妇产科医院', '').strip()
            parser.title = t

    # 备选作者
    if not parser.author:
        biz_m = re.search(r'var biz = "([^"]+)"', html)
        if biz_m:
            parser.author = '复旦大学附属妇产科医院'

    # 日期备选（ct 时间戳）
    if not parser.pub_date:
        ct_m = re.search(r'ct["\s:]+(\d{10})', html)
        if ct_m:
            try:
                import datetime
                t = datetime.datetime.fromtimestamp(int(ct_m.group(1)))
                parser.pub_date = t.strftime('%Y-%m-%d')
            except Exception:
                pass

    return {
        'title':   parser.title or '未知标题',
        'author':  parser.author or '复旦大学附属妇产科医院',
        'date':    parser.pub_date or '',
        'images':  list(dict.fromkeys(parser.images)),
        'body':    parser.body_paras,
    }, None

# ════════════════════════════════════════════════════════
# Markdown 生成
# ════════════════════════════════════════════════════════
def build_markdown(article, url, pub_date):
    lines = []
    lines.append(f"# {article['title']}\n")
    lines.append(f"- **公众号**: {article['author']}")
    lines.append(f"- **发布日期**: {pub_date}")
    lines.append(f"- **原文链接**: {url}\n")
    lines.append("## 正文\n")
    for para in article['body']:
        para = para.strip()
        if not para:
            continue
        lines.append(para)
        lines.append("")
    for img in article['images'][:20]:
        lines.append(f"![图片]({img})")
        lines.append("")
    return '\n'.join(lines)

# ════════════════════════════════════════════════════════
# 主程序
# ════════════════════════════════════════════════════════
def main():
    if len(sys.argv) < 2:
        print("❌ 请提供 xlsx 文件路径")
        print("  用法: python3 scripts/batch_http.py [xlsx路径]")
        sys.exit(1)

    XLSX_PATH = os.path.abspath(sys.argv[1])

    if not os.path.exists(XLSX_PATH):
        print(f"❌ 文件不存在: {XLSX_PATH}")
        sys.exit(1)

    # 安全检查：拒绝系统目录中的文件
    xlsx_abs = os.path.abspath(XLSX_PATH)
    unsafe_dirs = ('/etc', '/usr', '/bin', '/sbin', '/sys', '/proc', '/root')
    if any(xlsx_abs.startswith(d + '/') for d in unsafe_dirs):
        print(f"❌ 拒绝不安全的路径: {XLSX_PATH}")
        sys.exit(1)

    wb = openpyxl.load_workbook(XLSX_PATH)
    ws = wb.active
    rows = list(ws.iter_rows(min_row=2, values_only=True))
    total = len(rows)
    print(f"共读取 {total} 条记录 → 输出目录: {OUT_DIR}\n")

    success, failed = 0, []

    for i, row in enumerate(rows, 1):
        title    = str(row[1]).strip() if row[1] else f'文章{i}'
        url       = str(row[5]).strip() if row[5] else ''
        date_v    = row[2]
        pub_date  = parse_date(date_v)

        if not url or 'mp.weixin.qq.com' not in url:
            print(f"[{i}/{total}] 跳过（无效URL）: {title[:40]}")
            continue

        safe = sanitize(title)
        print(f"[{i}/{total}] {'='*40}")
        print(f"  标题: {title[:50]}")
        print(f"  日期: {pub_date}")
        print(f"  URL:  {url[:80]}")

        article, err = fetch_wx_article(url)
        if err or not article:
            print(f"  ❌ HTTP 失败: {err}")
            failed.append((i, title, url))
            time.sleep(2)
            continue

        # 保存 Markdown
        md_file = f"{pub_date}_{safe}.md"
        md_path = os.path.join(OUT_DIR, md_file)
        md_content = build_markdown(article, url, pub_date)
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        print(f"  ✅ Markdown: {md_file} ({len(article['images'])} 张图片)")

        success += 1
        print()
        time.sleep(1)

    print(f"\n{'='*60}")
    print(f"完成！Markdown: {success} 篇")
    if failed:
        print(f"失败: {len(failed)} 篇")
        for _, t, u in failed:
            print(f"  - {t}: {u[:60]}")
    print(f"\n提示: PDF 需手动用 Chrome 打开 Markdown 中的原文链接打印")
    print(f"      或改用 batch_scrape.py（需浏览器）")
    print(f"输出目录: {OUT_DIR}")

if __name__ == '__main__':
    main()
