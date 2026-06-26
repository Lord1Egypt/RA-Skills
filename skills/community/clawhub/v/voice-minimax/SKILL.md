# voice-minimax - 语音生成技能

MiniMax TTS 生成语音 → lark-cli 发送到飞书

## 配置

发布前需替换以下占位符：
- `你的MiniMax API Key` → 你的 MiniMax API Key
- `飞书用户ID` → 飞书用户 open_id（默认：ou_c1e599d5838a3f2ab8c4dbc40b709cf2）

## 默认行为（OPUS 语音条）

用户只说"生成语音"时，默认用这个流程：

```bash
# 1. TTS 生成 MP3（Python）
python3 -c "
import urllib.request, json

MINIMAX_KEY = '你的MiniMax API Key'

data = json.dumps({
    'model': 'speech-2.8-hd',
    'text': '文字内容',
    'stream': False,
    'voice_setting': {'voice_id': 'male-qn-qingse', 'speed': 1},
    'audio_setting': {'sample_rate': 32000, 'bitrate': 128000, 'format': 'mp3'}
}).encode()

req = urllib.request.Request(
    'https://api.minimaxi.com/v1/t2a_v2',
    data=data,
    headers={'Authorization': f'Bearer {MINIMAX_KEY}', 'Content-Type': 'application/json'}
)

with urllib.request.urlopen(req) as resp:
    result = json.load(resp)

audio_hex = result['data']['audio']
audio_bytes = bytes.fromhex(audio_hex)
with open('/tmp/voice.mp3', 'wb') as f:
    f.write(audio_bytes)
"

# 2. 转 OPUS
ffmpeg -i /tmp/voice.mp3 -c:a libopus -ar 16000 -ac 1 -b:a 64k -vbr off -map_metadata -1 -bitexact /tmp/voice.opus -y

# 3. 发语音条
cp /tmp/voice.opus ./voice.opus
lark-cli --as bot im +messages-send \
  --user-id 飞书用户ID \
  --msg-type audio \
  --audio ./voice.opus
```

---

## 选项：MP3 文件（需明确说"文件形式"/"可转发"）

用户说"文件形式"或"要能转发"时用这个：
```bash
cp /tmp/voice.mp3 ./voice.mp3
lark-cli --as bot im +messages-send \
  --user-id 飞书用户ID \
  --msg-type file \
  --file ./voice.mp3
```

## 关键参数

| 参数 | 值 |
|------|-----|
| MiniMax API | https://api.minimaxi.com/v1/t2a_v2 |
| Model | speech-2.8-hd（不是 speech-01-turbo）|
| Voice ID | male-qn-qingse |
| OPUS 采样率 | 16000 Hz |
| OPUS 码率 | 64 kbps |
| OPUS vbr | off |

## 坑

1. **必须 `--as bot`**：默认 user identity 发到错误会话，看不到
2. **OPUS 参数**：16000Hz mono 64kbps vbr=off，否则 duration=0
3. **MiniMax model**：要用 `speech-2.8-hd`，不是 `speech-01-turbo`

## 适用场景
- 语音自我介绍
- 重要消息朗读
- 内容播报
