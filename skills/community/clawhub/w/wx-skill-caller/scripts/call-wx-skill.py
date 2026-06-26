#!/usr/bin/env python3
"""
Call wx skill API with user message content.
"""

import sys
import json
import urllib.request
import urllib.error

API_URL = "https://test-gig-c-api.1haozc.com/api/wx/kjj/v1/customer/skill/call"

def call_wx_skill(content: str) -> dict:
    """Call the wx skill API with the given content."""
    payload = {
        "content": content
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        API_URL,
        data=data,
        headers={
            "Content-Type": "application/json"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result
    except urllib.error.HTTPError as e:
        return {
            "error": f"HTTP Error {e.code}: {e.reason}",
            "status": e.code
        }
    except urllib.error.URLError as e:
        return {
            "error": f"URL Error: {e.reason}",
            "status": None
        }
    except json.JSONDecodeError as e:
        return {
            "error": f"JSON Decode Error: {str(e)}",
            "status": None
        }
    except Exception as e:
        return {
            "error": f"Unexpected Error: {str(e)}",
            "status": None
        }

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No content provided"}, ensure_ascii=False))
        sys.exit(1)

    content = sys.argv[1]
    result = call_wx_skill(content)
    print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    main()
