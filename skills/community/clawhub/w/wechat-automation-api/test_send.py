# -*- coding: utf-8 -*-
import requests
import json

url = "http://127.0.0.1:8808/"

data = {
    "token": "B3S6GiMbIPW1nX4VrK8JTkuEhoFcON9t",
    "action": "sendtext",
    "to": ["文件传输助手"],
    "content": "【来财测试】你好！如果收到这条消息，说明微信自动化部署成功！🎉"
}

print("正在发送测试消息...")
response = requests.post(url, json=data)
print("发送结果：")
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
