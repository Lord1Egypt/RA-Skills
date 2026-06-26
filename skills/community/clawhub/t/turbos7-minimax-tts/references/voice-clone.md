# 音色快速复刻 API 参考

## 基础信息

- **API 地址**: `https://api.minimaxi.com/v1/voice_clone`
- **认证**: Bearer Token
- **说明**: 复刻音色 7 天内未调用会被系统删除

## 复刻流程

1. **上传音频文件** → 获取 `file_id`
2. **调用复刻接口** → 获取复刻音色 `voice_id`
3. **使用复刻音色** → 进行语音合成

## 请求体

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `file_id` | int | 是 | 待复刻音频的 file_id |
| `voice_id` | string | 是 | 自定义音色 ID |
| `clone_prompt` | object | 否 | 示例音频（增强稳定性） |
| `text` | string | 否 | 试听文本（最长 1000 字符） |
| `model` | string | 否* | 试听使用的模型（*传 text 时必填） |
| `need_noise_reduction` | bool | 否 | 降噪，默认 false |
| `need_volume_normalization` | bool | 否 | 音量归一化，默认 false |
| `aigc_watermark` | bool | 否 | 添加水印，默认 false |

### clone_prompt

| 参数 | 类型 | 说明 |
|------|------|------|
| `prompt_audio` | int | 示例音频 file_id |
| `prompt_text` | string | 示例音频对应文本 |

### voice_id 规则

- 长度范围: [8, 256]
- 首字符必须为英文字母
- 允许数字、字母、-、_
- 末位字符不可为 -、_
- 不可与已有 ID 重复

## 音频要求

| 项目 | 要求 |
|------|------|
| 格式 | mp3, m4a, wav |
| 时长 | 10 秒 ~ 5 分钟 |
| 大小 | 不超过 20 MB |

### 示例音频要求

| 项目 | 要求 |
|------|------|
| 时长 | 小于 8 秒 |
| 大小 | 不超过 20 MB |

## 错误码

| 错误码 | 说明 |
|--------|------|
| 0 | 成功 |
| 1000 | 未知错误 |
| 1001 | 超时 |
| 1002 | 限流 |
| 1004 | 鉴权失败 |
| 1013 | 服务内部错误 |
| 2013 | 输入格式错误 |
| 2038 | 无复刻权限（需账号认证） |

## 使用示例

### 基本复刻

```python
import requests
import os

API_KEY = os.getenv("MINIMAX_API_KEY")

response = requests.post(
    "https://api.minimaxi.com/v1/voice_clone",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "file_id": 123456789,
        "voice_id": "my_custom_voice",
        "need_noise_reduction": False,
        "need_volume_normalization": False
    }
)

result = response.json()
print(f"状态: {result['base_resp']['status_msg']}")
```

### 带试听的复刻

```python
response = requests.post(
    "https://api.minimaxi.com/v1/voice_clone",
    headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
    json={
        "file_id": 123456789,
        "voice_id": "my_custom_voice",
        "clone_prompt": {
            "prompt_audio": 987654321,
            "prompt_text": "This voice sounds natural and pleasant."
        },
        "text": "A gentle breeze sweeps across the soft grass.",
        "model": "speech-2.8-hd",
        "need_noise_reduction": True
    }
)

result = response.json()
demo_audio = result.get("demo_audio", "")
if demo_audio:
    print(f"试听音频: {demo_audio}")
```
