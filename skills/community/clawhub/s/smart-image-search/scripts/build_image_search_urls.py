#!/usr/bin/env python3
import json
import sys
from urllib.parse import quote


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: build_image_search_urls.py <query>", file=sys.stderr)
        return 1

    query = " ".join(sys.argv[1:]).strip()
    encoded = quote(query, safe="")
    data = {
        "query": query,
        "encoded_query": encoded,
        "bing_images": f"https://www.bing.com/images/search?q={encoded}",
        "baidu_images": f"https://image.baidu.com/search/index?tn=baiduimage&word={encoded}",
        "sogou_images": f"https://pic.sogou.com/pics?query={encoded}",
    }
    print(json.dumps(data, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
