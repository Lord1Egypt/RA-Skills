---
name: xhs-sentry
description: 面向中文用户的小红书舆情巡检技能。按关键词抓取搜索结果，判断登录墙/验证码/空结果状态，输出结构化笔记、热度/风险/竞品信号和现场截图。使用前需配置 XHS_COOKIE 与消息接收渠道（如 Telegram、企业微信）。适用于品牌口碑监控、竞品观察、热点追踪与内容研究。
---

# 小红书舆情哨兵

用于快速查看某个关键词在小红书上的讨论现场。输出内容包括：
- 页面状态判断（正常 / 登录墙 / 验证码 / 空结果）
- 结构化笔记信息（标题、作者、点赞、日期、链接、封面）
- 热度 / 风险 / 竞品信号
- 现场截图

适合用于：品牌口碑监控、竞品观察、热点追踪、内容研究。

注意：这是**快速巡检型技能**，核心价值是“现场取证 + 初步判断”，不是严格的情感分析模型。

## 执行

```bash
NODE_PATH=$(npm root -g) node {baseDir}/scripts/monitor.js "<关键词>" <数量> {baseDir}/tmp
```

## 读结果

优先读取这些字段：
- `status.auth_mode`
- `status.needsLogin`
- `status.captcha`
- `status.noResult`
- `notes`
- `analysis.overall`
- `analysis.summary`
- `analysis.top_hot`
- `analysis.top_risk`
- `diagnostics.body_preview`

## 登录态

默认优先复用已有小红书登录态：
- 先读环境变量 `XHS_COOKIE`
- 若没有，再回退读取现有脚本中的 `export XHS_COOKIE="..."`

因此这个 Skill 会自动兼容你已有的 `xhs-monitor` cookie 配置。`status.auth_mode` 会标明当前使用的是：
- `env-cookie`
- `script-cookie:<script>`
- `anonymous`

## 消息接收渠道

`xhs-sentry` 本身负责巡检与输出结构化结果；如果要把结果自动发到聊天工具，还需要配置消息接收渠道。

常见示例：

### Telegram
```bash
export CHANNEL="telegram"
export TARGET_ID="telegram:YOUR_TELEGRAM_ID"
```

### 企业微信（WeCom）
```bash
export CHANNEL="wecom"
export TARGET_ID="wecom:YOUR_WECOM_ID"
```

说明：
- Telegram 数字 ID 可通过 `@userinfobot` 获取
- 企业微信接收 ID 需与你当前 OpenClaw / wecom 通道配置一致
- 所有真实 ID 都不应写入公开仓库，应使用占位符

## 输出规则

### 1. 先判断页面状态，再下业务结论
- 若 `needsLogin=true` 或 `captcha=true`，明确说明这是平台拦截，**不是无舆情**。
- 若 `noResult=true` 且截图一致，可判断当前关键词结果为空。
- 若 `notes.length===0` 但无明确空结果提示，说明更可能是页面结构漂移或风控侧拦截。

### 2. 有结果时输出舆情摘要
**格式要求**：直接输出报告正文，绝对不需要任何聊天语气、打招呼或上下文废话。
**重要规则**：提到任何笔记时，必须使用 Markdown 格式附上真实的超链接，格式如：`[《笔记标题》](真实URL)`，绝对不能只放文本。
【特别注意：输出结果禁止寒暄，禁止说“任务已重跑”、“以下是报告”等废话，直接给出报告正文。任何引用笔记必须加上真实超链接 [《标题》](URL)】

至少回答：
- 总体倾向：`analysis.overall`
- 摘要：`analysis.summary`
- 最值得关注的热度笔记 1-3 条
- 最值得关注的风险笔记 1-3 条

### 3. 信号定义
- `risk-watch`：负面/避雷/翻车/维权类信号较多
- `hot-trend`：爆款/高赞/刷屏类信号较多
- `competitive-discussion`：对比/平替/测评类内容较多
- `neutral-chatter`：有讨论，但没有明显风险或爆点
- `insufficient-data`：没抓到足够内容，不能下结论

### 4. 必须附截图
始终附上现场截图：
```text
MEDIA: {baseDir}/tmp/xhs_sentry_*.png
MEDIA: {baseDir}/tmp/xhs_login_*.png
MEDIA: {baseDir}/tmp/xhs_captcha_*.png
MEDIA: {baseDir}/tmp/xhs_empty_*.png
MEDIA: {baseDir}/tmp/xhs_error_*.png
```

## 注意
- 这是一层**启发式舆情哨兵**，适合快速巡检，不等于严肃情感分析模型。
- 不要把空数组直接解释成“没有讨论”，必须结合状态和截图。
- 小红书结构变动频繁；若结果异常，优先信截图和 `body_preview`。
