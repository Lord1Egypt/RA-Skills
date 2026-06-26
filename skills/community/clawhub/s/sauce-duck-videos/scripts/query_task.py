#!/usr/bin/env python3
"""
查询RunningHub任务状态
用法: python query_task.py <HOST> <API_KEY> <TASK_ID>
"""

import sys
import json
import urllib.request
import urllib.error


def query_task(host: str, api_key: str, task_id: str) -> dict:
    """查询任务状态"""
    url = f"https://{host}/openapi/v2/query"

    headers = {
        "Host": host,
        "Authorization": f"Bearer {api_key}"
    }

    data = {
        "taskId": task_id
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers=headers,
        method="POST"
    )

    with urllib.request.urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def main():
    if len(sys.argv) != 4:
        print("Usage: python query_task.py <HOST> <API_KEY> <TASK_ID>", file=sys.stderr)
        sys.exit(1)

    host = sys.argv[1]
    api_key = sys.argv[2]
    task_id = sys.argv[3]

    try:
        result = query_task(host, api_key, task_id)
        print(json.dumps(result, ensure_ascii=False))
    except urllib.error.HTTPError as e:
        error_response = {
            "status": "FAILED",
            "errorCode": str(e.code),
            "errorMessage": str(e.reason),
            "taskId": task_id
        }
        try:
            body = json.loads(e.read().decode("utf-8"))
            error_response["errorMessage"] = body.get("msg", str(e.reason))
        except:
            pass
        print(json.dumps(error_response, ensure_ascii=False))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({
            "status": "FAILED",
            "errorCode": "-1",
            "errorMessage": str(e),
            "taskId": task_id
        }, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()