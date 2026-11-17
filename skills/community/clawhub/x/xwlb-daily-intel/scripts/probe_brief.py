#!/usr/bin/env python3
# 探针：提取央视视频页 video_brief div（快讯子条目全文兜底）
import re, sys, urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"

def probe(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    html = urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "ignore")
    m = re.search(r'class="video_brief"[^>]*>(.*?)</div>', html, re.S)
    if not m:
        return None, "NO_DIV"
    text = re.sub(r"<[^>]+>", "", m.group(1))
    text = re.sub(r"\s+", " ", text).strip()
    # 检查页面更新时间
    t = re.search(r'id="content"_Ptime[^>]*>(.*?)<|Ptime["\']?\s*[:=]\s*["\']([^"\']+)', html)
    return text, (t.group(1) or t.group(2)) if t else ""

if __name__ == "__main__":
    for url in sys.argv[1:]:
        try:
            text, info = probe(url)
            vid = url.rsplit("/", 1)[-1].replace(".shtml", "")
            if text is None:
                print(f"[{vid[:20]}] {info}")
            elif text:
                print(f"[{vid[:20]}] BRIEF({len(text)}字): {text[:2000]}")
            else:
                print(f"[{vid[:20]}] EMPTY_BRIEF updtime={info}")
        except Exception as e:
            print(f"[{url[-24:]}] ERROR: {e}")
        print("---")
