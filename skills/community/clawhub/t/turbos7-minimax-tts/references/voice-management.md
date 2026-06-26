# 音色管理 API 参考

## 查询可用音色

- **API**: `POST https://api.minimaxi.com/v1/get_voice`
- **认证**: Bearer Token

### 请求体

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `voice_type` | string | 是 | 音色类型 |

### voice_type 选项

| 值 | 说明 |
|----|------|
| `system` | 系统音色 |
| `voice_cloning` | 快速复刻音色（需调用后才可查询） |
| `voice_generation` | 文生音色 |
| `all` | 全部 |

### 响应体

```json
{
  "system_voice": [
    {
      "voice_id": "Chinese (Mandarin)_Reliable_Executive",
      "voice_name": "沉稳高管",
      "description": ["一位沉稳可靠的中年男性高管声音..."]
    }
  ],
  "voice_cloning": [...],
  "voice_generation": [...],
  "base_resp": {"status_code": 0, "status_msg": "success"}
}
```

---

## 删除音色

- **API**: `POST https://api.minimaxi.com/v1/del_voice`
- **认证**: Bearer Token

### 请求体

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `voice_id` | string | 是 | 要删除的音色 ID |

### 响应体

```json
{
  "base_resp": {"status_code": 0, "status_msg": "success"}
}
```

## 使用示例

### 查询全部音色

```python
import requests
import os

API_KEY = os.getenv("MINIMAX_API_KEY")

response = requests.post(
    "https://api.minimaxi.com/v1/get_voice",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    },
    json={"voice_type": "all"}
)

result = response.json()

print("=== 系统音色 ===")
for v in result.get("system_voice", []):
    print(f"  {v['voice_id']}: {v.get('voice_name', '')}")

print("\n=== 复刻音色 ===")
for v in result.get("voice_cloning", []):
    print(f"  {v['voice_id']}")

print("\n=== 文生音色 ===")
for v in result.get("voice_generation", []):
    print(f"  {v['voice_id']}")
```

### 删除音色

```python
response = requests.post(
    "https://api.minimaxi.com/v1/del_voice",
    headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
    json={"voice_id": "my_custom_voice"}
)

result = response.json()
print(f"删除结果: {result['base_resp']['status_msg']}")
```

## 注意事项

- 快速复刻的音色为**未激活状态**，需正式调用一次才可在 `voice_cloning` 中查询到
- 删除后该音色将无法恢复
