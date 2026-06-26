# -*- coding: utf-8 -*-
import sys, io, platform
if platform.system() == 'Windows':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

"""
url2pdf-mk 统一入口：智能路由
  • 1 个 URL  → 单篇抓取（scrape.py），PDF + Markdown 完整保留
  • ≥2 个 URL 或 xlsx → 批量抓取（batch_scrape.py），PDF + Markdown 全量生成

用法：
  py scripts/main.py <URL>                                       # 单篇
  py scripts/main.py <URL1> <URL2> <URL3> ...                    # 多篇
  py scripts/main.py /path/to/list.xlsx                          # xlsx 批量
  py scripts/main.py data.json <URL1> <URL2> ...                # 带标题的批量（JSON 放标题，顺序对应）

作者：qkz | 2026-04-13
"""
import sys, os, subprocess, platform, tempfile, openpyxl, json as _json

SYSTEM = platform.system()
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))

# 调用子脚本时注入环境变量（强制入口检查）
ENV_MAIN = {**os.environ, 'URL2PDFMK_ENTRY': 'main'}

# ══════════════════════════════════════════════════════════════
# 0. 检测 Chrome 是否可用
# ══════════════════════════════════════════════════════════════
def chrome_available():
    if SYSTEM == 'Windows':
        paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        ]
        return any(os.path.isfile(p) for p in paths)
    elif SYSTEM == 'Darwin':
        return os.path.isfile('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
    else:
        for p in ('chromium', 'chromium-browser', 'google-chrome'):
            try:
                subprocess.run([p, '--version'], capture_output=True, timeout=5)
                return True
            except Exception:
                pass
        return False

# ══════════════════════════════════════════════════════════════
# 1. 分析参数，判断处理模式
# ══════════════════════════════════════════════════════════════
def analyze_args(args):
    """
    返回:
      mode: 'single' | 'batch_xlsx' | 'batch_urls'
      urls: [str]
      json_path: str|None   # JSON 文件路径（供 batch_urls 读取标题用）
      xlsx_path: str|None
      isolated: bool        # 是否使用隔离模式
    """
    # 检查是否有 --isolated 参数
    isolated = '--isolated' in args
    args = [a for a in args if a != '--isolated']

    if not args:
        return None, [], None, None, isolated

    first = args[0]

    if first.endswith('.xlsx') or first.endswith('.xls'):
        return 'batch_xlsx', [], None, first, isolated

    # 检查是否有 JSON 文件（用于提供标题）
    json_path = None
    for a in args:
        if a.endswith('.json') and os.path.isfile(os.path.abspath(a)):
            json_path = os.path.abspath(a)
            break

    urls = []
    for a in args:
        s = str(a).strip()
        if s and ('mp.weixin.qq.com' in s or s.startswith('http') or s.startswith('https://')):
            urls.append(s if s.startswith('http') else f'https://{s}')

    if len(urls) == 0:
        return None, [], None, None, isolated
    elif len(urls) == 1:
        return 'single', urls, None, None, isolated
    else:
        return 'batch_urls', urls, json_path, None, isolated

# ══════════════════════════════════════════════════════════════
# 2. 生成临时 xlsx
# ══════════════════════════════════════════════════════════════
def urls_to_xlsx(items):
    """
    将 (title, url) 列表写入临时 xlsx，格式与 batch_scrape.py 兼容：
    col[1]=标题(B), col[2]=日期(C), col[5]=URL(F)
    items: list of (title, url) tuples
    """
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "URL列表"
    headers = ['logo', '标题', '日期', '摘要', '标签', 'URL']
    ws.append(headers)
    for title, url in items:
        ws.append(['', title, '', '', '', url])
    tmp = tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False)
    wb.save(tmp.name)
    tmp.close()
    return tmp.name

# ══════════════════════════════════════════════════════════════
# 3. 主路由
# ══════════════════════════════════════════════════════════════
def main():
    args = sys.argv[1:]

    if not args:
        print("❌ 未提供参数")
        print(__doc__)
        print("选项:")
        print("  --isolated    使用隔离浏览器 Profile（无 Cookie/登录态）")
        sys.exit(1)

    mode, urls, json_path, xlsx_path, isolated = analyze_args(args)

    if mode is None:
        print("❌ 未识别到有效的 URL")
        print(__doc__)
        sys.exit(1)

    # 构建子进程参数
    isolated_arg = ['--isolated'] if isolated else []

    # ── 单篇模式 ────────────────────────────────────────────────
    if mode == 'single':
        url = urls[0]
        print(f"📌 单篇模式（URL=1）")
        if isolated:
            print(f"   🔒 隔离模式：不使用浏览器登录态")
        print(f"   使用 scrape.py 完整抓取（PDF + Markdown）")
        print(f"   URL: {url[:80]}")
        print()
        ret = subprocess.run(
            [sys.executable, os.path.join(SKILL_DIR, 'scrape.py'), url] + isolated_arg,
            cwd=SKILL_DIR,
            env=ENV_MAIN
        )
        sys.exit(ret.returncode)

    # ── 批量 xlsx 模式 ───────────────────────────────────────────
    elif mode == 'batch_xlsx':
        xlsx_path = os.path.abspath(xlsx_path)

        try:
            wb = openpyxl.load_workbook(xlsx_path, read_only=True)
            ws = wb.active
            rows = list(ws.iter_rows(min_row=2, values_only=True))
            wb.close()
        except Exception as e:
            print(f"❌ 无法读取 xlsx: {e}")
            sys.exit(1)

        url_count = sum(1 for r in rows if r[5] and str(r[5]).strip())
        print(f"📦 批量模式（xlsx，检测到 {url_count} 个 URL）")
        if isolated:
            print(f"   🔒 隔离模式：不使用浏览器登录态")

        if url_count == 0:
            print("❌ xlsx 中未找到有效 URL（第6列 F）")
            sys.exit(1)
        elif url_count == 1:
            print(f"   ⚡ 仅 1 个 URL，降级为 scrape.py 单篇模式")
            row = next(r for r in rows if r[5] and str(r[5]).strip())
            url = str(row[5]).strip()
            ret = subprocess.run(
                [sys.executable, os.path.join(SKILL_DIR, 'scrape.py'), url] + isolated_arg,
                cwd=SKILL_DIR,
                env=ENV_MAIN
            )
            sys.exit(ret.returncode)

        use_chrome = chrome_available()
        script = 'batch_scrape.py' if use_chrome else 'batch_http.py'
        print(f"   使用 {script}（Chrome {'可用' if use_chrome else '不可用'}）")
        print()
        ret = subprocess.run(
            [sys.executable, os.path.join(SKILL_DIR, script), xlsx_path] + isolated_arg,
            cwd=SKILL_DIR,
            env=ENV_MAIN
        )
        sys.exit(ret.returncode)

    # ── 批量多 URL 模式 ──────────────────────────────────────────
    elif mode == 'batch_urls':
        url_count = len(urls)
        print(f"📦 批量模式（{url_count} 个 URL）")
        if isolated:
            print(f"   🔒 隔离模式：不使用浏览器登录态")

        if url_count == 1:
            print(f"   ⚡ 仅 1 个 URL，降级为 scrape.py 单篇模式")
            ret = subprocess.run(
                [sys.executable, os.path.join(SKILL_DIR, 'scrape.py'), urls[0]] + isolated_arg,
                cwd=SKILL_DIR,
                env=ENV_MAIN
            )
            sys.exit(ret.returncode)

        # 从 JSON 文件读取标题（支持 list 或 dict 格式）
        items = []
        json_data = None
        if json_path:
            try:
                with open(json_path, encoding='utf-8') as f:
                    json_data = _json.load(f)
                print(f"   📄 从 JSON 读取标题: {os.path.basename(json_path)}")
            except Exception as e:
                print(f"   ⚠️  JSON 读取失败: {e}，使用默认标题")

        for i, url in enumerate(urls):
            title = f'文章{i+1}'
            if json_data:
                if isinstance(json_data, list) and i < len(json_data):
                    title = str(json_data[i].get('title', title))
                elif isinstance(json_data, dict) and str(i) in json_data:
                    title = str(json_data[str(i)].get('title', title))
            items.append((title, url))

        print(f"   将 {url_count} 个 URL 写入临时 xlsx ...")
        tmp_xlsx = urls_to_xlsx(items)
        print(f"   临时文件: {tmp_xlsx}")
        print()

        use_chrome = chrome_available()
        script = 'batch_scrape.py' if use_chrome else 'batch_http.py'
        print(f"   使用 {script}（Chrome {'可用' if use_chrome else '不可用'}）")
        ret = subprocess.run(
            [sys.executable, os.path.join(SKILL_DIR, script), tmp_xlsx] + isolated_arg,
            cwd=SKILL_DIR,
            env=ENV_MAIN
        )
        # 清理临时 xlsx 文件
        try:
            os.remove(tmp_xlsx)
            print(f"   🧹 已清理临时文件: {tmp_xlsx}")
        except Exception as e:
            print(f"   ⚠️  清理临时文件失败: {e}")
        sys.exit(ret.returncode)

if __name__ == '__main__':
    main()
