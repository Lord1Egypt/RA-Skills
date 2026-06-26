# 2026-05-18｜Karpathy / Everything Claude Code 对 xz01 的适配结论

## 用户决策

用户确认按以下方向吸收：

- 吸收 Andrej Karpathy Claude Code 指南中的精准修改、简洁优先、目标驱动验证原则。
- Everything Claude Code 只吸收 hook/verification-loop 的设计思路。
- 安全扫描不需要作为 xz01 规则。
- 并行化暂时不需要；xz01 仍默认严格串行。
- hooks 内容可以直接做到 xz01 技能里，但必须是 xz01 专用守门，不是照搬 ECC 全量 hook 系统。

## 已沉淀到技能的规则

1. Dev prompt 应包含成功标准：目标页面/组件/缺陷、允许文件、禁止文件、清 runtime、test 验收标准。
2. Dev 必须精准修改：每一行改动都对应当前 xz01 验收目标；禁止顺手重构、顺手格式化、无关清理。
3. Dev 必须简洁实现：不增加未要求抽象、helper、复杂 JS 或新架构。
4. 官方通过只能来自独立 test 截图 + AI 视觉 + 必要 rule 审核，dev 自测不能替代 test。
5. xz01 hook-style gates 只用于边界和门禁：pre-dev、post-dev、pre-test、post-test、pre-package。
6. hook gate 禁止事项：写 `/root/.openclaw`、改 `demo_xz01`、改 PHP/backend/controller/model/config/route/core/vendor、未清 runtime 进入验证、缺截图/AI 就 test PASS、缺静态/HTTP/截图/AI/rule 就打包。

## 脚本

新增：

```text
scripts/xz01-hook-gate.py
```

用途：手动调用，或未来接入 Claude Code hooks / Hermes profile / Kanban worker / cron watchdog。脚本自身不安装 hook，不执行通用安全扫描，不引入并行化。

## 不做的事

- 不把 Everything Claude Code 全量安装到当前环境。
- 不启用 AgentShield/security-scan 作为 xz01 必需流程。
- 不启用 multi-agent 并行化。
- 不让 hooks 替代 test 的 PC+移动端截图和 AI 视觉分析。
- 不让 hooks 写入 `/root/.openclaw`。
