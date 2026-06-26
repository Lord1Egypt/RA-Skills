# 豆包 TTS 2.0 API 参考

## 基础信息

| 参数 | 值 |
|------|-----|
| Endpoint | `https://openspeech.bytedance.com/api/v1/tts` |
| Auth | `Bearer; {ACCESS_TOKEN}`（**分号**，不是空格） |
| Operation | `query`（**非流式**，不是 submit） |
| Cluster | `volcano_tts` |

## 请求格式

```python
POST https://openspeech.bytedance.com/api/v1/tts
Headers:
  Authorization: Bearer; {ACCESS_TOKEN}
  Content-Type: application/json
Body:
{
  "app": {
    "appid": "8982709936",
    "token": "{ACCESS_TOKEN}",
    "cluster": "volcano_tts"
  },
  "user": {
    "uid": "zhongshu_tts"
  },
  "audio": {
    "voice_type": "zh_female_xiaohe_uranus_bigtts",
    "encoding": "mp3",
    "speed_ratio": 1.0,
    "volume_ratio": 1.0,
    "pitch_ratio": 1.0,
    "emotion": "neutral"
  },
  "request": {
    "reqid": "{uuid4}",
    "text": "要合成的文本",
    "text_type": "plain",
    "operation": "query"
  }
}
```

## 响应格式

```json
{
  "code": 3000,
  "message": "success",
  "data": "{base64编码的MP3音频数据}"
}
```

- `code=3000` 表示成功
- 其他 code 表示失败
- 音频数据是 base64 编码的 MP3

## 可用音色（voice_type）

### 女声
| 音色 | voice_type | 适用场景 |
|------|-----------|---------|
| 小何（默认）| `zh_female_xiaohe_uranus_bigtts` | 通用，清晰自然 |
| 撒娇学妹 | `zh_female_sajiaoxuemei_uranus_bigtts` | 软萌可爱 |
| 温柔淑女 | `zh_female_wenroushunv_uranus_bigtts` | 轻柔温柔 |
| 高冷御姐 | `zh_female_gaolengyujie_uranus_bigtts` | 成熟御姐 |
| 清新女声 | `zh_female_qingxinnvsheng_uranus_bigtts` | 清新自然 |
| 魅力苏菲 | `zh_female_sophie_uranus_bigtts` | 有气质 |
| Vivi | `zh_female_vv_uranus_bigtts` | 多语言 |

### 男声
| 音色 | voice_type | 适用场景 |
|------|-----------|---------|
| 云舟 | `zh_male_m191_uranus_bigtts` | 清晰通用 |
| 霸气青叔 | `zh_male_baqiqingshu_uranus_bigtts` | 有气场 |
| 深夜播客 | `zh_male_shenyeboke_uranus_bigtts` | 低沉磁性 |

## 可用情绪（emotion）

`neutral` | `happy` | `sad` | `tender` | `excited` | `lovey-dovey` | `storytelling` | `radio` | `angry` | `fear` | `hate` | `surprised` | `coldness` | `shy` | `ASMR` | `news` | `advertising`

## 常见错误

| 错误 | 原因 | 解决 |
|------|------|------|
| `code=10001` | Token 无效 | 检查 ACCESS_TOKEN 是否正确 |
| `code=10002` | APPID 不存在 | 检查 APPID = `8982709936` |
| `code=10003` | 无 TTS 配额 | 在火山引擎控制台开通服务 |
| `no available instance` | APPID 未开通 TTS 服务 | 联系火山引擎技术支持 |

## 播放方式

```bash
# macOS 使用 afplay（自动路由到系统默认输出）
afplay /tmp/voice_xxx.mp3

# 也可用 Python 播放
subprocess.run(["afplay", mp3_path])
```
