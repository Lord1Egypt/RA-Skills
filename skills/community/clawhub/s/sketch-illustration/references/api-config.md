# API 配置

> 建议：把真实 `TOKEN` 放在 `scripts/apimart.env`（本地文件），不要写进文档/仓库或聊天记录。

## ZenMux（主用）
```
API_URL: https://api.zenmux.ai/v1/images/generations
MODEL: google/gemini-3-pro-image-preview
TOKEN: <从 openclaw.json 读取>
SIZE: 16:9
RESOLUTION: 2K (或 4K 用于高密度信息图)
N: 1
```

## apimart.ai（备用）
```
API_URL: https://api.apimart.ai/v1/images/generations
MODEL: gemini-3-pro-image-preview (或 imagen-3, dall-e-3)
TOKEN: <YOUR_TOKEN>
SIZE: 16:9
RESOLUTION: 2K (或 4K)
N: 1
```

## 使用示例（apimart）

```python
import requests
import time

url = "https://api.apimart.ai/v1/images/generations"
task_url = "https://api.apimart.ai/v1/tasks/"

payload = {
    "model": "gemini-3-pro-image-preview",
    "prompt": "Your prompt here",
    "size": "16:9",
    "n": 1,
    "resolution": "2K"
}

headers = {
    "Authorization": "Bearer <token>",
    "Content-Type": "application/json"
}

# Submit task
response = requests.post(url, json=payload, headers=headers)
data = response.json()
task_id = data["data"][0]["task_id"]

# Poll for result
for i in range(30):
    time.sleep(2)
    poll_resp = requests.get(f"{task_url}{task_id}", headers=headers)
    poll_data = poll_resp.json()
    status = poll_data["data"]["status"]
    
    if status == "completed":
        img_url = poll_data["data"]["url"]
        # Download image
        img_resp = requests.get(img_url, timeout=60)
        with open("output.png", "wb") as f:
            f.write(img_resp.content)
        break
    elif status == "failed":
        print(f"Failed: {poll_data}")
        break
```

## 注意事项

1. **apimart 是异步接口** — 需要轮询 task 状态获取结果
2. **gemini-3-pro-image-preview 在 apimart 上可能不稳定** — 如遇失败可尝试 `imagen-3` 或 `dall-e-3`
3. **size 参数** — 使用 `"16:9"` 生成横图（不要传 1:1）
4. **resolution 参数** — `"2K"` 适合普通插图，`"4K"` 适合高密度信息大图
5. **ZenMux 额度** — 每 5 小时重置一次，用完自动恢复
