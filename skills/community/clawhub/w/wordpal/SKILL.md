---
name: WordPal
description: 嵌在聊天框的个性化英语学习 companion。结合你与龙虾的memory出词，学习英语词汇learn，查看词汇报告report。含17种多样题型，配合AI解析，覆盖多种词汇学习状态。使用FSRS算法计算复习周期，并通过corn定时推送学习提醒。
user-invocable: true
metadata:
  openclaw:
    emoji: "📘"
    requires:
      bins:
        - node
    capabilities:
      - cron
---
# WordPal · 主控协议

## 技能目录约定
- `{baseDir}` 由 OpenClaw 自动替换为本技能的实际安装路径

## 执行顺序
1. 执行 `session-context.js --mode <learn|report>`：
   - `profile_exists = false` → 读取 `references/onboarding.md` 引导onboarding初始化
   - `profile_exists = true` → `data.profile` 为用户画像唯一真值，继续流程
2. 判断用户意图并路由：
   - learn（学习意图，或只输入 `/wordpal`）→ 读 `references/learn.md`
   - report（报告意图）→ 读 `references/report.md`

## 事件映射
- 答对 → `submit-answer.js --word "<word>" --event correct --last-reviewed <YYYY-MM-DD> [--op-id <op_id>]`
- 答错 → 先调用 `show-hint.js --word "<word>"` 获取 `hint_token`，展示解析后按 B-3 子流程判定，**不直接提交**
- 提示后记住 → `submit-answer.js --word "<word>" --event remembered_after_hint --hint-token <token> --last-reviewed <YYYY-MM-DD> [--op-id <op_id>]`
- 提示后仍不会 → `submit-answer.js --word "<word>" --event wrong --hint-token <token> --last-reviewed <YYYY-MM-DD> [--op-id <op_id>]`
- 跳过/会了/斩词 → `submit-answer.js --word "<word>" --event skip --last-reviewed <YYYY-MM-DD> [--op-id <op_id>]`

`<word>` 为当前题目单词，`<YYYY-MM-DD>` 为今日日期，`<op_id>` 来自 `next-question.js` 返回的 `data.stage.op_id`（可选）。
`<token>` 来自 `show-hint.js` 返回的 `data.hint_token`，一次性有效；缺失时 submit-answer.js 返回 `HINT_TOKEN_REQUIRED` 错误。
`remembered_after_hint` vs `wrong` 判定见 `learn.md`「阶段 B-3」。

## 脚本通用规则
- 所有脚本前缀：`node {baseDir}/scripts/`
- 成功返回 `{ meta, data }` JSON
- 脚本失败统一兜底：`系统暂时不可用，请稍后再试。`

## 禁止项
- 不要直接操作 SQLite 词库文件或输出内部表快照。
- 不要跳过脚本直接改词条。
