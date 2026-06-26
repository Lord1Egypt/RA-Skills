import requests
import json
import pathlib

def get_qmsg_key():
    cfg = pathlib.Path(__file__).parent / "secrets.json"
    return json.loads(cfg.read_text())["qmsg"]["key"]

def send_qmsg(message: str) -> dict:
    key = get_qmsg_key()
    url = f"https://qmsg.zendee.cn/send/{key}"
    try:
        r = requests.get(url, params={"msg": message}, timeout=10)
        return r.json()
    except Exception as e:
        return {"success": False, "reason": str(e)}

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("用法: python qmsg_push.py <消息内容>")
        sys.exit(1)
    result = send_qmsg(sys.argv[1])
    print(result)
