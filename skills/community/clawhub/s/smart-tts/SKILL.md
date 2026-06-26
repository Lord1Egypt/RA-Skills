---
name: smart-tts
description: 智能语音合成。自动尝试多种模型/音色，直到成功。解决 418 资源未开通问题。
---

# Smart TTS - 智能语音合成

自动尝试多种模型和音色组合，直到成功生成语音。

## 使用方法

### 1. 配置 API Key

在环境中设置：
```bash
# Windows
set DASHSCOPE_API_KEY=你的百炼APIKey

# 或在 openclaw.json 中配置
```

### 2. 生成语音

```bash
python skills/smart-tts/scripts/generate.py "要生成的文字"
```

### 3. 批量生成

```bash
python skills/smart-tts/scripts/batch.py
```

## 可用音色

| 模型 | 音色 | 特点 |
|------|------|------|
| cosyvoice-v2 | longshao_v2 | 成熟稳重男 |
| cosyvoice-v2 | longanyang | 阳光大男孩 |
| cosyvoice-v3-flash | longanyang | 阳光大男孩 |
| cosyvoice-v3-flash | longanhuan | 欢脱元气女 |
| cosyvoice-v3-flash | longhuhu_v3 | 天真烂漫女童 |
| cosyvoice-v3-flash | longpaopao_v3 | 飞天泡泡音 |
| cosyvoice-v3-flash | longjielidou_v3 | 阳光顽皮男 |

## 工作原理

1. 按优先级依次尝试不同的模型+音色组合
2. 遇到 418 资源未开通错误自动切换下一个
3. 成功生成语音后自动保存
4. 全部失败则报错

## 输出路径

默认保存到：`~/.openclaw/workspace/tts_output.wav`
