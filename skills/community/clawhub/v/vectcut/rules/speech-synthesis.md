---
name: speech-synthesis
description: 将文字合成为语音音频。调用VectCut开放平台的 generate_speech 接口，传入文本和音色 ID，返回合成后的音频结果。当用户提到文字转语音、语音合成、TTS、配音、朗读文本、生成音频旁白，或者需要把一段文字变成语音文件时，使用此 skill。即使用户没有明确说"语音合成"，只要意图是把文字变成可播放的语音，都应该触发。
---

# Speech Synthesis（文字合成语音）

通过VectCut开放平台 API 将文本转换为语音音频。

## 使用场景

- 用户有一段文字，想转成语音
- 用户需要为视频配音
- 用户想试听某个音色的效果

## 前置条件

用户需要提供：
1. 待合成的文本内容（`text`）
2. 音色 ID（`voice_id`）
3. 可用登录态（环境变量 `VECTCUT_API_KEY`）

如果用户没有提供其中任何一项，主动询问。

## API 调用方式

接口地址：`https://open.vectcut.com/cut_jianying/generate_speech`

请求方法：POST

请求头：
```
Content-Type: application/json
Authorization: Bearer $VECTCUT_API_KEY
Accept: */*
Host: open.vectcut.com
Connection: keep-alive
```

请求体：
```json
{
  "text": "待合成的文本",
  "provider": "fish",
  "voice_id": "音色ID"
}
```

## 执行步骤

1. 确认用户已提供 `text`、`voice_id`；然后检查 `VECTCUT_API_KEY` 是否存在
2. 若 `VECTCUT_API_KEY` 缺失，必须先调用 `vectcut-login` 技能完成登录与 token 校验，再继续
3. 使用 curl 发送 POST 请求：
2. 使用 curl 发送 POST 请求：
curl --location --request POST 'https://open.vectcut.com/cut_jianying/generate_speech' \
  --header 'Content-Type: application/json' \
  --header 'Authorization: Bearer <API_KEY>' \
  --header "Authorization: Bearer ${VECTCUT_API_KEY}" \
  --header 'Host: open.vectcut.com' \
  --header 'Connection: keep-alive' \
  --data-raw '{
  --data-raw '{
    "text": "<TEXT>",
    "provider": "fish",
    "voice_id": "<VOICE_ID>"
  }'
```

4. 将接口返回结果展示给用户
5. 如果返回中包含音频 URL，告知用户可以下载或试听

## 注意事项

- `provider` 固定为 `"fish"`，无需用户指定
- 如果请求失败，先检查是否已通过 `vectcut-login` 设置了有效 `VECTCUT_API_KEY`，再检查 `voice_id` 是否正确
- 文本过长时建议分段合成
