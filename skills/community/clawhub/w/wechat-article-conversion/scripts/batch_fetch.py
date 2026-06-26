"""
批量抓取微信文章
用法:
  python batch_fetch.py <urls_file> [formats_csv]
  python batch_fetch.py <urls_file> markdown,html,json
formats_csv: 逗号分隔的格式列表，默认 markdown
"""
import sys
import os
import re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from fetch_article import fetch_article, save_article


def parse_urls(raw: str) -> list:
    """从字符串中提取所有微信文章URL（去重）"""
    urls = re.findall(r'https://mp\.weixin\.qq\.com/s/[a-zA-Z0-9_-]+', raw)
    seen = set()
    result = []
    for u in urls:
        if u not in seen:
            seen.add(u)
            result.append(u)
    return result


def parse_formats(raw: str) -> list:
    """解析用户输入的格式（支持数字序号或名称，单选或多选）"""
    fmt_map = {
        '1': 'markdown', '2': 'excel', '3': 'html', '4': 'text', '5': 'json',
        'markdown': 'markdown', 'excel': 'excel', 'html': 'html',
        'text': 'text', 'txt': 'text', 'json': 'json',
    }
    normalized = re.sub(r'[，、\s+和]+', ',', raw.strip().lower())
    parts = [p.strip() for p in normalized.split(',') if p.strip()]
    formats = []
    for p in parts:
        fmt = fmt_map.get(p, p)
        if fmt in ('markdown', 'excel', 'html', 'text', 'json') and fmt not in formats:
            formats.append(fmt)
        elif p not in formats:
            formats.append(p)
    return formats


def fetch_batch(urls: list, formats: list, output_dir: str = None) -> dict:
    """
    批量抓取文章，每篇文章按每种格式保存到 output_dir。

    注意：每篇每格式各抓一次（网络IO），暂不支持复用 content。
    如需优化，可将 fetch_article 拆分为 fetch(只请求网络) + convert(只做格式转换)。
    """
    if output_dir is None:
        output_dir = os.path.join(os.path.expanduser("~"), "Desktop", "微信文章批量")
    os.makedirs(output_dir, exist_ok=True)

    success = []   # [(title, [(format, filepath), ...]), ...]
    failed = []    # [(url, error), ...]

    for i, url in enumerate(urls, 1):
        print(f"[{i}/{len(urls)}] 抓取: {url[:60]}...", flush=True)
        try:
            # 每篇每格式各抓一次（fetch_article 内部无缓存，网络请求不可避免）
            title = None
            files = []
            for fmt in formats:
                try:
                    article = fetch_article(url, fmt)
                    if title is None:
                        title = article["title"]
                    fp = save_article(article, output_dir)
                    files.append((fmt, fp))
                    print(f"  [{fmt}] {os.path.basename(fp)}", flush=True)
                except Exception as e:
                    print(f"  [{fmt}] 失败: {e}", flush=True)
            if title and files:
                success.append((title, files))
        except Exception as e:
            failed.append((url, str(e)))
            print(f"  失败: {e}", flush=True)

    return {"success": success, "failed": failed, "total": len(urls), "formats": formats}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python batch_fetch.py <urls_file> [formats_csv]")
        sys.exit(1)

    urls_file = sys.argv[1]
    formats_raw = sys.argv[2] if len(sys.argv) > 2 else "markdown"

    with open(urls_file, encoding="utf-8") as f:
        raw = f.read()

    urls = parse_urls(raw)
    formats = parse_formats(formats_raw)

    if not urls:
        print("未找到微信文章链接")
        sys.exit(1)
    if not formats:
        print(f"无效的格式: {formats_raw}，可选: markdown, html, text, json, excel")
        sys.exit(1)

    print(f"找到 {len(urls)} 篇文章，格式: {formats}，开始批量抓取...", flush=True)
    result = fetch_batch(urls, formats)

    print("\n" + "=" * 50)
    print(f"成功: {len(result['success'])}/{result['total']} 篇")
    print(f"失败: {len(result['failed'])}")
    for title, files in result["success"]:
        print(f"\n  {title[:40]}")
        for fmt, fp in files:
            size = os.path.getsize(fp)
            print(f"    [{fmt}] {os.path.basename(fp)} ({size//1024}KB)")

    if result['failed']:
        print("\n失败列表:")
        for url, err in result['failed']:
            print(f"  - {url[:60]}: {err}")
