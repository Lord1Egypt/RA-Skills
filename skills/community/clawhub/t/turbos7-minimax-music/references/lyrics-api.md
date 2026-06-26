# MiniMax 歌词生成 API 参考

## 基础信息

- **API 地址**: `https://api.minimaxi.com/v1/lyrics_generation`
- **认证**: Bearer Token
- **API Key**: [MiniMax 平台 - 接口密钥](https://platform.minimaxi.com/user-center/basic-information/interface-key)

## 请求头

| Header | 必填 | 说明 |
|--------|------|------|
| `Content-Type` | 是 | `application/json` |
| `Authorization` | 是 | `Bearer {API_KEY}` |

## 请求体 (GenerateLyricsReq)

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `mode` | string | 是 | - | `write_full_song` 或 `edit` |
| `prompt` | string | 否 | 空 | 歌曲主题/风格，最长 2000 字符 |
| `lyrics` | string | 否 | - | 现有歌词，仅 `edit` 模式，最长 3500 字符 |
| `title` | string | 否 | - | 指定歌曲标题 |

## 响应体 (GenerateLyricsResp)

```json
{
  "song_title": "生成的歌名",
  "style_tags": "Pop, Upbeat, Female Vocals",
  "lyrics": "[Intro]\n(Ooh-ooh-ooh)\n\n[Verse 1]\n歌词内容...",
  "base_resp": {
    "status_code": 0,
    "status_msg": "success"
  }
}
```

## 支持的结构标签

| 标签 | 说明 |
|------|------|
| `[Intro]` | 前奏 |
| `[Verse]` | 主歌 |
| `[Pre-Chorus]` | 预副歌 |
| `[Chorus]` | 副歌/高潮 |
| `[Hook]` | 钩子 |
| `[Drop]` |  drop 部分 |
| `[Bridge]` | 桥段 |
| `[Solo]` | 独奏/说唱段 |
| `[Build-up]` | 渐进 |
| `[Instrumental]` | 纯器乐 |
| `[Breakdown]` | 分解 |
| `[Break]` | 停顿 |
| `[Interlude]` | 间奏 |
| `[Outro]` | 尾奏 |

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

### 示例 1: 生成完整歌词

```python
import requests
import os

API_KEY = os.getenv("MINIMAX_API_KEY")

response = requests.post(
    "https://api.minimaxi.com/v1/lyrics_generation",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "mode": "write_full_song",
        "prompt": "一首关于离别和重逢的民谣歌曲，温柔忧伤"
    }
)

result = response.json()
print(f"歌名: {result['song_title']}")
print(f"风格: {result['style_tags']}")
print(f"歌词:\n{result['lyrics']}")
```

### 示例 2: 续写歌词

```python
response = requests.post(
    "https://api.minimaxi.com/v1/lyrics_generation",
    headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
    json={
        "mode": "edit",
        "prompt": "继续往更深情的方向发展",
        "lyrics": "[Verse 1]\n海风轻轻吹\n\n[Chorus]\n永远在一起"
    }
)
```

### 示例 3: 指定标题

```python
response = requests.post(
    "https://api.minimaxi.com/v1/lyrics_generation",
    headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
    json={
        "mode": "write_full_song",
        "prompt": "关于星空和梦想的歌曲",
        "title": "星海之梦"
    }
)
```
