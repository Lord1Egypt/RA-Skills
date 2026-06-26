# MiniMax 音乐生成 API 参考

## 基础信息

- **API 地址**: `https://api.minimaxi.com/v1/music_generation`
- **认证**: Bearer Token
- **API Key**: [MiniMax 平台 - 接口密钥](https://platform.minimaxi.com/user-center/basic-information/interface-key)

## 请求头

| Header | 必填 | 说明 |
|--------|------|------|
| `Content-Type` | 是 | `application/json` |
| `Authorization` | 是 | `Bearer {API_KEY}` |

## 模型说明

| 模型 | 说明 | 限制 |
|------|------|------|
| `music-2.6` | 文本生成音乐（推荐） | Token Plan/付费用户，RPM 高 |
| `music-cover` | 基于参考音频生成翻唱 | Token Plan/付费用户，RPM 高 |
| `music-2.6-free` | 限免版 | 所有用户，RPM 低 |
| `music-cover-free` | 翻唱限免版 | 所有用户，RPM 低 |

## 请求体 (GenerateMusicReq)

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `model` | string | 是 | - | 模型名称 |
| `prompt` | string | 是* | - | 音乐描述，最长 2000 字符 |
| `lyrics` | string | 是* | - | 歌词，最长 3500 字符 |
| `is_instrumental` | boolean | 否 | false | 是否生成纯音乐 |
| `stream` | boolean | 否 | false | 是否流式传输 |
| `output_format` | string | 否 | hex | `url` 或 `hex` |
| `audio_url` | string | 否 | - | 参考音频 URL（翻唱用） |
| `audio_base64` | string | 否 | - | 参考音频 Base64（翻唱用） |
| `lyrics_optimizer` | boolean | 否 | false | 自动生成歌词 |
| `aigc_watermark` | boolean | 否 | false | 添加水印 |
| `audio_setting` | object | 否 | - | 音频配置 |

*纯音乐（is_instrumental=true）时 lyrics 非必填
*非纯音乐时 lyrics 必填

## audio_setting 参数

| 参数 | 可选值 |
|------|--------|
| `sample_rate` | 16000, 24000, 32000, 44100 |
| `bitrate` | 32000, 64000, 128000, 256000 |
| `format` | mp3, wav, pcm |

## 参考音频要求（music-cover）

| 项目 | 要求 |
|------|------|
| 时长 | 6 秒至 6 分钟 |
| 大小 | 最大 50 MB |
| 格式 | mp3, wav, flac 等 |

## 响应体 (GenerateMusicResp)

```json
{
  "data": {
    "status": 2,
    "audio": "hex编码的音频数据"
  },
  "trace_id": "04ede0ab069fb1ba8be5156a24b1e081",
  "extra_info": {
    "music_duration": 25364,
    "music_sample_rate": 44100,
    "music_channel": 2,
    "bitrate": 256000,
    "music_size": 813651
  },
  "base_resp": {
    "status_code": 0,
    "status_msg": "success"
  }
}
```

### status 状态码

| 值 | 说明 |
|----|------|
| 1 | 合成中 |
| 2 | 已完成 |

## 错误码

| 错误码 | 说明 |
|--------|------|
| 0 | 成功 |
| 1002 | 触发限流 |
| 1004 | 鉴权失败 |
| 1008 | 余额不足 |
| 1026 | 敏感内容 |
| 2013 | 参数异常 |
| 2049 | 无效 API Key |

## 使用示例

### 示例 1: 基于歌词生成歌曲

```python
import requests
import os

API_KEY = os.getenv("MINIMAX_API_KEY")

response = requests.post(
    "https://api.minimaxi.com/v1/music_generation",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "model": "music-2.6",
        "prompt": "独立民谣,忧郁,内省,渴望,独自漫步,咖啡馆",
        "lyrics": "[verse]\n街灯微亮晚风轻抚\n影子拉长独自漫步\n旧外套裹着深深忧郁\n\n[chorus]\n推开木门香气弥漫\n熟悉的角落陌生人看",
        "output_format": "url"
    }
)

result = response.json()
audio_url = result["data"]["audio"]
print(f"歌曲地址: {audio_url}")
```

### 示例 2: 生成纯音乐

```python
response = requests.post(
    "https://api.minimaxi.com/v1/music_generation",
    headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
    json={
        "model": "music-2.6",
        "prompt": "轻快的钢琴曲,阳光,春天,愉悦",
        "is_instrumental": True,
        "output_format": "url"
    }
)
```

### 示例 3: 指定音频格式

```python
response = requests.post(
    "https://api.minimaxi.com/v1/music_generation",
    headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
    json={
        "model": "music-2.6",
        "prompt": "电子音乐,动感,健身",
        "lyrics": "[verse]\n动起来别停下",
        "output_format": "url",
        "audio_setting": {
            "sample_rate": 44100,
            "bitrate": 256000,
            "format": "mp3"
        }
    }
)
```

### 示例 4: 生成翻唱版本

```python
response = requests.post(
    "https://api.minimaxi.com/v1/music_generation",
    headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
    json={
        "model": "music-cover",
        "prompt": "爵士风格,慵懒,夜晚酒吧",
        "audio_url": "https://example.com/reference.mp3"
    }
)
```
