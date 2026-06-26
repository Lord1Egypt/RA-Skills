# Workspace snippets

Use these snippets in the target agent workspace.

## IDENTITY.md

```md
## 🎤 Voice
- 默认语音：**zh-CN-XiaoxiaoNeural**（按 agent 角色替换）
- 模式：**语音对语音，文字对文字**
- 生成方式：`edge-tts`（全局脚本可用）
```

Recommended voice examples:
- 温暖女声：`zh-CN-XiaoxiaoNeural`
- 活泼女声：`zh-CN-XiaoyiNeural`
- 沉稳男声：`zh-CN-YunyangNeural`

## SOUL.md

```md
## Voice Conversation Mode (语音对话模式)

- 🎤 用户发语音 → 我用 **Edge TTS** 生成语音回复
- ⌨️ 用户发文字 → 我默认文字回复

**实现要点：**
1. 识别消息是否为语音（voice/audio）
2. 语音输入时，生成回复后调用 edge-tts 输出语音文件
3. 用消息通道发送语音消息

_这条规则用于保证“语音对语音，文字对文字”的体验一致性。_
```

## TOOLS.md

```md
### TTS (Edge)

- 引擎：**edge-tts**
- 脚本：`~/workspace/scripts/edge-tts.sh "文本" [输出文件] [声音]`
- 默认语音：按 agent 角色配置
- 模式：语音对语音，文字对文字
```

## Validation checklist

- 发一条文字，确认回复仍然是文字
- 发一条语音，确认回复变成语音
- 确认语音内容可听清，且语言/音色符合 agent 设定
