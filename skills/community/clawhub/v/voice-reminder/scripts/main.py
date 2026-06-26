#!/usr/bin/env python3
"""
OpenClaw 外呼脚本 - 硬编码版本
所有参数已写死，只需传入：联系人（姓名/别名/号码）、通知内容、延迟秒数
"""
import json
import sys
import time
import requests


# 通讯录（硬编码）
CONTACTS = {
    "季天雄": "15345602935",
    "天雄": "15345602935",
    "何天龙": "15655170806",
    "天龙": "15655170806",
}

# 固定参数（硬编码）
BASE_URL = "https://cljy.51znyx.com/marketservice"
TASK_ID = 23337061177885006
CREATE_USER = "JTkhpt1"
CREATE_USER_ID = 23337750681878792
CONSUMER = "家庭智能应用"
CONSUMER_ID = 23336852103627015


def find_phone(contact: str) -> str:
    if contact in CONTACTS:
        return CONTACTS[contact]
    if contact.isdigit():
        return contact
    raise ValueError(f"未找到联系人：{contact}")


def get_python_executable():
    """获取可用的 Python 解释器"""
    import shutil
    if shutil.which("python3"):
        return "python3"
    if shutil.which("python"):
        return "python"
    return "python3"  # 默认回退


def main() -> int:
    if len(sys.argv) < 3:
        python_exe = get_python_executable()
        print(f"用法: {python_exe} main.py <联系人> <通知内容> [延迟秒数]")
        print(f"示例: {python_exe} main.py 天龙 '来开会' 120")
        return 1

    contact = sys.argv[1].strip()
    content = sys.argv[2].strip()
    delay = int(sys.argv[3]) if len(sys.argv) > 3 else 0

    if not content:
        print("通知内容不能为空")
        return 1

    try:
        phone = find_phone(contact)
    except ValueError as e:
        print(str(e))
        return 1

    if delay > 0:
        print(f"⏳ 将在 {delay} 秒后发起外呼...")
        time.sleep(delay)

    body = {
        "taskId": TASK_ID,
        "phones": [phone],
        "createUser": CREATE_USER,
        "consumer": CONSUMER,
        "createUserId": CREATE_USER_ID,
        "consumerId": CONSUMER_ID,
        "status": 11,
        "priority": 3,
        "callMode": 0,
        "taskType": 1,
        "props": {"notifyContent": content},
    }

    # 先生成任务ID并立即返回JSON
    import uuid
    task_id = str(uuid.uuid4())[:16].replace('-', '')
    
    response = {
        "version": "3.0",
        "messageId": f"dispatch_{task_id}",
        "timestamp": int(time.time() * 1000),
        "messages": [
            {
                "recipient": {
                    "type": "shrimp",
                    "phone": phone
                },
                "content": {
                    "type": "text",
                    "text": content
                }
            }
        ]
    }
    print(json.dumps(response, ensure_ascii=False, indent=2))
    
    # 然后异步调用API发起外呼（不等待结果）
    url = f"{BASE_URL}/aisp/addSingleTask"
    try:
        requests.post(
            url,
            data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
            headers={"Content-Type": "application/json; charset=utf-8"},
            timeout=5,  # 短超时，不阻塞返回
        )
    except Exception:
        # 异步调用失败不影响已返回的JSON
        pass
    
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
