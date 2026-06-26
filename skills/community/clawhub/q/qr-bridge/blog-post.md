# AI Agent 遇到二维码就抓瞎？我用 122 行 Swift 解决了

> 一个周末项目，解决了 AI 编程助手面对中国互联网二维码生态时的"最后一公里"问题。

## 起因：一张海报，一个报名链接，无尽的挫败

事情是这样的——我在朋友圈看到一张北京 AI Meetup 的海报，想报名参加。海报上有个二维码，扫一下就能填表。

问题是，我当时在用 Claude Code 做开发，顺手把海报截图丢给它："帮我看看这个二维码是什么链接。"

Claude 很认真地"看"了图片，告诉我："图片中有一个二维码。"

然后呢？**然后就没有然后了。**

AI 视觉模型能"看到"二维码，但它**解码不了**。它知道那是个二维码，但读不出里面的内容。就像一个能认出所有汉字长相、却不知道怎么念的人。

好，那我手动扫出 URL，把链接给 Claude，让它帮我看看报名表单长什么样？

```bash
curl -sL "https://xxx.weixin.qq.com/s/xxxxx"
```

返回一段 HTML，里面赫然写着：**"请在微信客户端打开链接"**。

死胡同。

## 真正的问题：不是解码，是"门"

这件事让我意识到，二维码对 AI Agent 来说其实是个**双重障碍**：

**第一层：解码。** AI 视觉模型看得到二维码但读不出来。这个问题本身不难——macOS 系统自带的 CoreImage 框架就能解码，完全不需要装任何第三方库。

**第二层：中国互联网的"门"。** 这才是真正麻烦的地方。国内的二维码生态，背后藏着各种封闭网关：

- **微信**：`weixin.qq.com` 域名，必须在微信内置浏览器打开
- **企业微信**：不但要在企微里打开，还得是该组织的成员
- **淘宝**：`tb.cn` 短链，JS 重定向到 `tbopen://` 协议，只有淘宝 App 能接
- **抖音**：`v.douyin.com` 短链，最终跳到 `snssdk://` 深度链接
- **小红书**：`xhslink.com` 短链，307 跳转后要求 App 打开

这些"门"的存在意味着，就算你解码拿到了 URL，一路 `curl` 追下去，最后大概率卡在某个 App 专属协议上，得到一个毫无意义的 HTML 空壳。

AI Agent 面对这种情况完全懵了——它不知道链接为什么打不开，更不知道该告诉用户怎么办。

## 解决方案：一条完整的侦察管线

所以我做了 **qr-bridge**，一个 Claude Code 技能（Skill），把整个链路打通：

```
图片 → 二维码解码 → URL → 重定向追踪 → 网关识别 → 诊断建议
```

核心是一个 **122 行的 Swift 脚本**，用 macOS 原生的 CoreImage 框架解码二维码。零依赖，编译后执行速度约 **10ms**。

### 看个真实例子

假设你给 Claude Code 一张包含二维码的海报图片，qr-bridge 会自动跑完整个流程：

**Step 1: 解码**

```bash
$ ./qr-decode poster.png
```

```json
{
  "ok": true,
  "count": 1,
  "results": [
    {
      "message": "https://mp.weixin.qq.com/s/AbCdEfGh",
      "symbology": "QRCode",
      "bounds": { "x": 40, "y": 40, "width": 290, "height": 290 }
    }
  ]
}
```

**Step 2: 追踪重定向链**

```
1. https://mp.weixin.qq.com/s/AbCdEfGh  → 302
2. https://open.weixin.qq.com/connect/oauth2/authorize?...  → 200
```

**Step 3: 网关识别 + 诊断**

```
## QR Bridge Diagnosis

**Decoded:** https://mp.weixin.qq.com/s/AbCdEfGh
**Gate type:** WeChat
**Why it fails:** 链接包含微信 OAuth 授权，必须在微信内置浏览器中打开
**What to do:** 用微信扫描原始二维码，直接在微信内打开
```

AI Agent 终于能告诉用户：这个链接打不开不是因为它坏了，而是因为它只能在微信里打开。**从"我不知道"变成了"我知道为什么，而且我能告诉你怎么办"。**

## 技术亮点

几个值得一提的设计选择：

- **macOS CoreImage 原生解码**：不依赖 Python 库，不需要 `brew install zbar`，系统自带就够了。编译一次后反复使用，每次解码约 10ms
- **结构化 JSON 输出**：AI Agent 友好，方便下游处理
- **122 行 Swift**：整个解码器只有 122 行，短到可以完整 review。核心逻辑就是 `CIDetector(ofType: CIDetectorTypeQRCode)`，剩下的都是输入校验和输出格式化
- **网关检测用模式匹配**：不靠 AI 猜测，而是对域名、响应头、页面内容做确定性的规则匹配。`weixin.qq.com` 就是微信，`tbopen://` 就是淘宝，没有歧义

## 什么是 Claude Code Skill？

简单说，Claude Code Skill 就是一份 Markdown 文档（`SKILL.md`），告诉 Claude Code 在特定场景下该调用什么工具、怎么调用。放到 `~/.claude/skills/` 目录下，Claude Code 就会在合适的时候自动激活它。

qr-bridge 作为一个 Skill，意味着你不需要记住任何命令。直接跟 Claude Code 说"帮我扫这张图的二维码"，它就知道该编译 Swift、调解码器、追链接、做诊断，最后给你一个完整的报告。

## 安装

```bash
# 克隆到技能目录
git clone https://github.com/Vicky-v7/qr-bridge.git ~/.claude/skills/qr-bridge

# 编译 Swift 解码器（一次就好）
bash ~/.claude/skills/qr-bridge/scripts/setup.sh
```

装完之后对 Claude Code 说 "扫一下这个二维码" 就行了。

## 最后

这个项目不大，但解决的是一个很实际的问题：**AI Agent 在中国互联网环境下，面对二维码和平台网关时的无力感。**

如果你也在用 Claude Code，遇到过类似的场景——丢给它一张截图，它只能告诉你"这里有个二维码"然后就卡住了——试试 qr-bridge。

GitHub: [https://github.com/Vicky-v7/qr-bridge](https://github.com/Vicky-v7/qr-bridge)

欢迎 Star、Issue、PR。

---

*作者：Vicky（刘维祺），AI 产品经理，偶尔写代码。*

---

**Tags:** `AI` `Claude Code` `QR Code` `macOS` `Swift` `CoreImage` `开源` `AI Agent` `二维码` `中国互联网`
