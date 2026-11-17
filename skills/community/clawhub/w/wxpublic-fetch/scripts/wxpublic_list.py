"""
用法: python3 wxpublic_list.py <app_id> <secure_key> <name> <startDate> <endDate>

查询微信公众号文章列表，将结果以 JSON 格式输出到 stdout。
成功时输出: {"urls": [...], "count": N}
失败时输出: {"error": "..."} 并以非零退出码退出。
"""

import json
import sys
import urllib.error
import urllib.request


def main():
    if len(sys.argv) != 6:
        print("用法: python3 wxpublic_list.py <app_id> <secure_key> <name> <startDate> <endDate>")
        sys.exit(1)

    app_id, secure_key, name, start_date, end_date = sys.argv[1:]

    payload = json.dumps(
        {
            "app_id": app_id,
            "secure_key": secure_key,
            "name": name,
            "startDate": start_date,
            "endDate": end_date,
        },
        ensure_ascii=False,
    ).encode("utf-8")

    req = urllib.request.Request(
        "https://wxpub.aibana.art/fetch",
        data=payload,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        try:
            data = json.loads(body)
        except Exception:
            data = {"error": f"HTTP {e.code}: {body}"}
    except Exception as e:
        data = {"error": str(e)}

    print(json.dumps(data, ensure_ascii=False))
    if "error" in data:
        sys.exit(1)


if __name__ == "__main__":
    main()
