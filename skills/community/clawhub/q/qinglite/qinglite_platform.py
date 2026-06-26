import requests
import json
import sys

def qinglite_login(mobile, code):
    url = "https://www.qinglite.cn/api/interface/user/user_mobile/login"
    payload = {
        "mobile": mobile,
        "code": code,
        "prefix": "+86",
        "act": 1,
        "app_type": "openclaw",
        "post_type": "ajax"
    }
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        response_json = response.json()

        if response_json.get("code") in [10000, 20000] and "token" in response_json.get("data", {}):
            token = response_json["data"]["token"]
            print(f"Login successful. Token: {token}")
            return token
        else:
            print(f"Login failed: {response_json.get('msg', 'Unknown error')}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None
    except json.JSONDecodeError:
        print(f"Failed to decode JSON from response: {response.text}")
        return None

def qinglite_publish(token, title, content, post_type, media=""):
    url = "https://www.qinglite.cn/api/interface/content/news/create"
    payload = {
        "title": title,
        "content": content,
        "type": post_type,
        "media": media,
        "token": token,
        "app_type": "openclaw"
    }
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        response_json = response.json()

        if response_json.get("code") in [10000, 20000]:
            print(f"Publish successful: {response_json.get('msg', 'Success')}")
            return True
        else:
            print(f"Publish failed: {response_json.get('msg', 'Unknown error')}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return False
    except json.JSONDecodeError:
        print(f"Failed to decode JSON from response: {response.text}")
        return False

if __name__ == "__main__":
    action = sys.argv[1]

    if action == "login":
        if len(sys.argv) != 4:
            print("Usage: python qinglite_platform.py login <mobile> <code>")
            sys.exit(1)
        mobile = sys.argv[2]
        code = sys.argv[3]
        qinglite_login(mobile, code)
    elif action == "publish":
        if len(sys.argv) < 6 or len(sys.argv) > 7:
            print("Usage: python qinglite_platform.py publish <token> <title> <content> <type> [media]")
            sys.exit(1)
        token = sys.argv[2]
        title = sys.argv[3]
        content = sys.argv[4]
        post_type = int(sys.argv[5])
        media = sys.argv[6] if len(sys.argv) == 7 else ""
        qinglite_publish(token, title, content, post_type, media)
    else:
        print("Invalid action. Use 'login' or 'publish'.")
        sys.exit(1)
