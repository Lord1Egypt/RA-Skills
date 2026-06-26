# STT - 语音识别 (Speech-to-Text)

将语音消息识别为文字。支持 ogg/wav/mp3/m4a 格式。

## 触发方式

- 用户发送语音消息时自动触发
- 或者手动调用 skill

## 功能

1. **自动识别语音** - 收到语音消息时自动转文字
2. **离线识别** - 使用 Faster-Whisper，无需网络
3. **格式转换** - 自动用 ffmpeg 转换音频格式

## 依赖

- Python 包: `faster-whisper`, `pydub`
- ffmpeg: `C:\ffmpeg\bin` (需要在系统 PATH 中)

## 安装

```bash
pip install faster-whisper pydub
```

## 使用示例

```
用户发送语音 → 自动识别为文字 → 根据文字内容回复
```

## 配置

- 模型大小: tiny (可改为 base/small/medium/large，精度更高但更慢)
- 默认语言: zh (中文)
- ffmpeg 路径: C:\ffmpeg\bin

## 原理

1. 接收语音文件 (ogg)
2. 用 ffmpeg 转换为 wav (16000Hz, mono)
3. 用 Faster-Whisper 识别为文字
4. 返回识别结果并继续对话