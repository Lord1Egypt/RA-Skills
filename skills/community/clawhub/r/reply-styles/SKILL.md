---
name: reply-styles
description: Draft high-EQ, style-controlled replies for chat, email, DMs, customer support, community operations, sales, and difficult conversations. Use when the user wants a reply rewritten in a specific tone without prompt-tuning. Model-agnostic, preset-style driven, no API key required.
version: 1.0.0
license: MIT-0
metadata:
  openclaw:
    emoji: "💬"
---

# Reply Styles

为用户生成高情商、风格化、可直接发送的回复文案。

核心定位：

- 模型无关
- 预置风格，不靠用户反复调教
- 同时支持高情商和明确边界
- 可用于私聊、邮件、客服、销售、社群、管理沟通

## 何时使用

- 用户说“帮我高情商回复一下”
- 用户要“委婉一点、坚定一点、像高管一点、像客服一点”
- 用户要回复客户、老板、同事、朋友、社群成员
- 用户要拒绝、安抚、催促、解释、道歉、成交、收口

## 工作方式

主 `SKILL.md` 只保留路由与规则。按需读取：

- 风格总览：`references/style-catalog.md`
- 场景映射：`references/scenario-map.md`
- 强度系统：`references/intensity-system.md`
- 渠道映射：`references/channel-map.md`
- 人格包：`references/persona-packs.md`
- 回复模式：`references/mode-packs.md`
- 通用原则：`references/core-rules.md`
- 风格示例：`references/style-examples.md`
- 效果验收：`references/effect-rubric.md`

如果要快速定位风格或场景，优先运行：

- `node scripts/get-style-bundle.mjs --list`
- `node scripts/get-style-bundle.mjs --style warm-professional`
- `node scripts/get-style-bundle.mjs --list-personas`
- `node scripts/get-style-bundle.mjs --list-modes`
- `node scripts/get-style-bundle.mjs --style warm-professional --intensity balanced --channel wechat`
- `node scripts/recommend-style.mjs --scene angry-customer --goal deescalate --channel support-ticket --persona calm-operator --mode soothe-first`
- `node scripts/scaffold-reply.mjs --style firm-boundary --scene reject-request --intensity soft --channel wechat --persona trusted-advisor --mode clear-reject`
- `node scripts/showcase-replies.mjs --scene reject-request --intent "礼貌拒绝继续无偿帮忙" --persona trusted-advisor --mode clear-reject`

## 生成原则

1. 先判断关系，再判断情绪温度，再判断风格、强度和渠道。
2. 高情商不等于软弱，不要为了“礼貌”牺牲边界。
3. 先保留用户真实意图，再做语气优化。
4. 默认输出一版可以直接发的正文；只有用户要求时再给多个版本。
5. 不要解释“我为什么这样写”，除非用户明确要分析。
6. 风格要稳定，不要一条回复里又像客服又像朋友。

## 最小决策流程

### Step 1：识别场景

从用户输入中提取：

- 对象：客户 / 老板 / 同事 / 朋友 / 社群成员 / 陌生人
- 目标：安抚 / 拒绝 / 催促 / 成交 / 道歉 / 解释 / 推进 / 收口
- 风险：对方生气 / 关系脆弱 / 场合正式 / 需要边界 / 需要成交
- 调性：温暖 / 专业 / 坚定 / 高级 / 轻松 / 干练

### Step 2：选风格

优先先跑脚本拿最小推荐结果，再读 `references/style-catalog.md`。

如果用户明确指定风格，再直接读取对应风格说明：

- `warm-professional`
- `high-eq-soft`
- `firm-boundary`
- `de-escalation`
- `executive-crisp`
- `founder-direct`
- `luxury-concierge`
- `community-manager`
- `premium-sales`
- `supportive-coach`
- `playful-friendly`
- `relationship-repair`
- `consultant-polished`
- `partner-diplomatic`
- `pr-safe`
- `recruiter-polite`
- `operations-push`
- `customer-success`
- `elder-respectful`
- `cool-minimal`
- `bookish-gentle`
- `service-recovery`
- `brand-host`
- `legal-clean`

### Step 3：选强度和渠道

优先读：

- `references/intensity-system.md`
- `references/channel-map.md`
- `references/persona-packs.md`
- `references/mode-packs.md`

默认：

- 强度：`balanced`
- 渠道：`wechat`
- 人格包：留空
- 回复模式：留空

### Step 4：按结构写回复

默认结构：

1. 开场先接住情绪或意图
2. 中段表达核心信息
3. 结尾给下一步或收口

### Step 5：对照原则自检

读 `references/core-rules.md` 和 `references/effect-rubric.md`，确保：

- 不油腻
- 不虚伪
- 不啰嗦
- 不失边界
- 适合实际发送
- 风格稳定
- 像真人会发的话

## 输出偏好

默认输出：

- 1 个成稿版本
- 直接可发送
- 不带多余解释
- 保持用户原意

用户如果要求，可额外提供：

- 更软一版
- 更硬一版
- 更短一版
- 更高级一版
- 邮件版 / 微信版 / 评论区版

## 不要这样做

- 不要一味加“哈哈”“呀”“呢”制造假高情商
- 不要把简单回复写成鸡汤
- 不要过度道歉
- 不要把坚定边界写成攻击
- 不要把销售感写成油腻推销
- 不要让风格压过信息本身

## 成功标准

这项 skill 的目标不是“变得更礼貌”，而是让用户觉得：

- 这句话像我想说的，只是更高级
- 既体面又有效
- 有风格，但不做作
- 不需要再自己手动调语气

当前系统支持：

- `24` 套主风格
- `6` 个人格包
- `6` 个回复模式
- `3` 档强度：`soft / balanced / sharp`
- `6` 个渠道：`wechat / email / dm / group / comment / support-ticket`
- 共 `24 × 6 × 6 × 3 × 6 = 15552` 种组合方式
