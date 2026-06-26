# QQ Bot 语音适配方案

## 何时阅读本文档

仅在以下情况阅读：

- 用户明确提到 `QQ Bot`、`QQBot`、`qqbot`
- 用户说 OpenClaw 的默认 CLI transcription 在 QQ Bot 1.5.4 下不生效
- 用户需要绕过 QQ Bot 插件自带的 STT / TTS 限制

这是一个兼容 QQ Bot 1.5.4 插件限制的绕行方案，不依赖 OpenClaw 默认的 CLI transcription。

## STT（用户语音 -> 文字）

使用手动转写方案：

1. **音频文件位置**
   - `/home/admin/.openclaw/qqbot/downloads/*.bin`
   - 这些 `.bin` 文件本质上是 WAV 格式

2. **匹配逻辑**
   - 用消息时间戳匹配 `downloads` 目录中修改时间最近的 `.bin` 文件

3. **转写命令**

```bash
LATEST_VOICE=$(ls -lt /home/admin/.openclaw/qqbot/downloads/*.bin 2>/dev/null | head -1 | awk '{print $NF}')
TENCENTCLOUD_SECRET_ID="xxx" TENCENTCLOUD_SECRET_KEY="xxx" TENCENTCLOUD_APPID="xxx" \
python3 /path/to/asr-sentence-recognition/scripts/flash_recognize.py "$LATEST_VOICE"
```

## TTS（文字 -> 语音回复）

不要走 QQ Bot 插件 TTS，直接用 skill 合成 + 标签发送：

1. **合成语音**
   - 使用 `tencentcloud-tts` skill

```bash
TENCENTCLOUD_SECRET_ID="xxx" TENCENTCLOUD_SECRET_KEY="xxx" \
python3 /path/to/tencentcloud-tts/scripts/tencent_tts.py "文本内容" --output /tmp/voice.mp3
```

2. **发送语音**
   - 在回复中使用：

```xml
<qqvoice>/tmp/voice.mp3</qqvoice>
```

## 前提条件

- 已安装 `asr-sentence-recognition` skill
- 已安装 `tencentcloud-tts` skill
- 已配置腾讯云密钥（环境变量或 shell profile）

## Agent 行为约束

- 不要向最终用户暴露背后的绕行实现
- 不要说“让我尝试手工转写”“我现在绕过插件限制”之类的话
- 对外表现为：系统正常支持 QQ Bot 的语音收发

## 适用边界

- 这里的 STT 默认调用 `flash_recognize.py`
- 如果后续 QQ Bot 的 `.bin` 文件来源、目录或插件行为变化，需要先重新验证文件落盘路径和格式
