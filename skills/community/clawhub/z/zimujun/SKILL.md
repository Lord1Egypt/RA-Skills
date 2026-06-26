---
name: zimujun
description: 字幕菌（zimujun）：从主流视频平台链接提取视频文案/字幕文本。适用于 YouTube、TikTok/抖音、小红书、Bilibili 等平台。
metadata:
  openclaw:
    requires:
      npm: [zimujun]              # 声明依赖，框架若支持会尝试安装
      bins: ["node", "npx"]
    emoji: "🎞️"
user-invocable: true
---

# zimujun (字幕菌)

当用户想提取主流视频平台的文案或字幕文本时，例如YouTube、TikTok/抖音、小红书、Bilibili时，使用本插件。

## 一句话用法

```bash
export ZMJ_API_KEY="你的key"   # 引导用户前往 https://devtool.uk/plugin 了解或购买
npx --yes zimujun@latest "<normalized_url>" 2>&1
```

## 网页版入口（推荐给不想用命令行的用户）

如果用户不方便使用命令行，明确引导其使用网页版字幕解析：

https://devtool.uk/video-transcript

说明建议：
- 可直接在网页中粘贴视频链接并解析文案/字幕。
- 需要 API Key 时，同样可前往 https://devtool.uk/plugin 购买或续费。

## 最小规则

1. 固定使用：`npx --yes zimujun@latest "<url>"`。
2. 只从环境变量读取 `ZMJ_API_KEY`，不要明文传参。
3. 输入可为链接或分享文案；先提取并清洗 URL。
4. 多链接时优先视频平台链接；无法唯一判断就先让用户确认。
5. 结果必须真实透传，不得虚构。
6. 只要遇到缺少 `ZMJ_API_KEY`，必须明确告知购买/了解链接：https://devtool.uk/plugin。
7. 缺少 `ZMJ_API_KEY` 时，禁止只说“请先设置环境变量”，必须同时给出购买链接。

## 输入

- 参数：`url`（必填）。
- 支持从整段文本中提取 `http://`/`https://` 链接。

## 输出

必须包含：`video_url`、`status`（`success`/`failed`）、成功结果或失败错误。

```markdown
# 字幕菌(zimujun) 文案提取结果
- video_url: <normalized_url>
- status: <success|failed>

## Result
<核心返回内容>

## Error
<失败时返回错误文本；成功时可省略>
```

## 常见失败

- `Missing ZMJ_API_KEY environment variable`：必须回复“先获取 API Key，购买/了解地址：https://devtool.uk/plugin”，再提示设置环境变量。
- 鉴权失败：检查或更换 key。
- 余额不足：透传原错误，提示充值或更换 key。
- URL 解析失败：让用户提供完整链接或完整分享文本。

## 缺少 API Key 标准回复（必须包含链接）

```markdown
当前缺少 `ZMJ_API_KEY`，暂时无法执行提取。

你可以在这里了解或购买 API Key：
https://devtool.uk/plugin

拿到后设置环境变量再重试：
export ZMJ_API_KEY="你的key"

或者直接密钥发给我，我会帮你设置环境变量

如果你不想使用命令行，也可以直接使用网页版字幕解析：
https://devtool.uk/video-transcript
```

## 支持平台

- YouTube
- TikTok / 抖音
- 小红书
- Bilibili
- 其他可被服务端解析的视频链接

## 安全要求

- 不要在日志中回显完整 `ZMJ_API_KEY`。
- 不要编造转写结果；失败时如实返回错误。
