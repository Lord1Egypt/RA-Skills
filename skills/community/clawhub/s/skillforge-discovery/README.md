# SkillForge OpenClaw Skill

自动发现和调用付费 AI 服务的 OpenClaw Skill。

## 功能

- 🔍 **能力缺口检测** - 自动分析任务需求，识别需要外部 API 的场景
- 🎯 **智能服务发现** - 从 SkillForge 平台发现匹配的付费服务
- 💰 **费用透明** - 调用前展示价格，用户确认后执行
- 📊 **使用统计** - 记录调用历史和费用

## 安装

```bash
# 复制到 OpenClaw skills 目录
cp -r skillforge-skill ~/.openclaw/skills/
```

## 配置

在 `~/.openclaw/config.yaml` 中添加：

```yaml
skills:
  skillforge:
    platform_url: "https://skillforge.example.com"
    api_key: "sk_xxxx"
    discover_limit: 3
    max_cost_per_call: 1.00
```

## 使用

### 1. 自动检测能力缺口

当 Agent 遇到需要外部 API 支持的任务时，Skill 会自动检测：

```
用户: 帮我生成一张猫的图片

Agent: [SkillForge] 检测到能力缺口: image_generation
       正在发现服务...
```

### 2. 手动发现服务

```
用户: 帮我找一个能翻译的 API

Agent: [SkillForge] 发现服务:
       1. DeepL Translate - $0.01/次 ⭐4.9
       2. Google Translate - $0.002/次 ⭐4.7
```

### 3. 调用服务

```
用户: 用第一个翻译 "Hello World"

Agent: [SkillForge] 调用 DeepL Translate...
       结果: "你好世界"
       费用: $0.01，余额: $12.50
```

## API

### handler(context)

主入口函数。

```javascript
// 检测能力缺口
const result = await handler({
  task: "帮我生成一张图片"
});

// 发现服务
const result = await handler({
  action: "discover",
  capability: "image_generation"
});

// 调用服务
const result = await handler({
  action: "invoke",
  serviceId: "svc_xxx",
  input: { prompt: "a cat in space" }
});
```

### detectCapabilityGap(task)

检测任务中的能力缺口。

```javascript
const capabilities = detectCapabilityGap("帮我翻译这段文字");
// ["text_translation"]
```

### discoverServices(capability, limit?)

发现匹配的服务。

```javascript
const result = await discoverServices("image_generation", 5);
```

### invokeService(serviceId, input, options?)

调用服务。

```javascript
const result = await invokeService("svc_xxx", {
  prompt: "a cat in space"
});
```

## 支持的能力

| 能力 | 关键词 |
|------|--------|
| image_generation | 生成图片, create image, DALL-E |
| speech_synthesis | 语音合成, TTS, 文字转语音 |
| speech_recognition | 语音识别, 转录 |
| text_translation | 翻译, translate |
| web_search | 网页搜索, web search |
| pdf_processing | PDF处理, PDF提取 |
| ocr | OCR, 文字识别 |
| ... | 更多见 handler.js |

## 错误处理

| 错误码 | 说明 |
|--------|------|
| SERVICE_NOT_FOUND | 服务不存在 |
| SERVICE_OFFLINE | 服务离线 |
| INSUFFICIENT_BALANCE | 余额不足 |
| INVOCATION_ERROR | 调用失败 |

## 开发

```bash
# 安装依赖（开发时）
npm install

# 运行测试
npm test
```

## 许可证

MIT