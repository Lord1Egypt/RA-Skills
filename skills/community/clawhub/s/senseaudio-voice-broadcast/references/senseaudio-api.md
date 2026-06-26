# SenseAudio TTS 接入说明

## 接口

- URL: `https://api.senseaudio.cn/v1/t2a_v2`
- Method: `POST`
- Header:
  - `Authorization: Bearer <API_KEY>`
  - `Content-Type: application/json`

## 最小请求体

```json
{
  "model": "SenseAudio-TTS-1.0",
  "text": "你好，欢迎体验 SenseAudio 带来的极致语音服务。",
  "voice_setting": {
    "voice_id": "male_0004_a"
  }
}
```

## Skill 内推荐流程

1. 先把原始文本改写成适合 TTS 的口播文本
2. 再确定 `voice_id`
3. 再调用 `scripts/senseaudio_tts.py`
4. 保存输出音频到本地路径

## 推荐环境变量

- `SENSEAUDIO_API_KEY`: SenseAudio API key

## 推荐调用示例

```bash
export SENSEAUDIO_API_KEY="your_api_key"

python3 scripts/senseaudio_tts.py \
  --text "你好，欢迎来到今晚的陪伴时刻。" \
  --voice-id male_0004_a \
  --output ./senseaudio_output.wav
```

## 使用建议

- 先做人物化改写，再送入 TTS
- 文本太长时优先分段
- 陪伴型内容适合偏慢语速和更柔和的措辞
- 播报型内容优先保证信息清晰
