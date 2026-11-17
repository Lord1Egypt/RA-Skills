# summarize — 保存与恢复操作（v11.0）

仅在用户明确要求 `总结 保存` / `summarize save` 时读取并执行本文件。默认总结和诊断均为只读。

## 保存前检查

1. 读取当前工作区的 `AGENTS.md` 或同级写入规则。
2. 按以下顺序确定项目根目录：用户明确指定的项目根目录；客户端当前工作区根目录；当前目录的 `git rev-parse --show-toplevel`。候选不唯一、与用户指定任务冲突或无法确定时，不写入。
3. 清除密钥、访问令牌、个人数据、完整原始对话和未经验证的推测；先用 `scripts/save_handoff.py --check-only` 拦截常见凭据模式。
4. 将报告限制为目标、状态、证据、决策、阻塞和下一步，并以首行 schema=2 元数据开头：`<!-- summarize-handoff schema=2 {JSON} -->`。JSON 必须包含 `created_at`、`task_id`、`project_root`、`branch`、`head`、`goal_digest`。`task_id` 使用安全短标识；`goal_digest` 使用规范化目标文本的 SHA-256 十六进制摘要（可截取至少 12 位）。

## 保存位置与方式

- 快捷入口为 `{项目根目录}/.transfers/latest.md`，真实报告保存到 `.transfers/handoffs/{task_id}.md`；`latest.md` 只保存当前报告指针。
- 用 `python scripts/save_handoff.py --input <已生成的临时报告> --output {项目根目录}/.transfers/latest.md` 写入。脚本拒绝常见密钥、邮箱、手机号、Cookie、带密码连接串、原始对话转储和不安全 task_id，保留 `latest.md.bak`，使用锁和临时文件原子替换。
- 写入后读取指针和 `.transfers/handoffs/{task_id}.md`，并运行 `python scripts/save_handoff.py --input <报告路径> --check-only` 回测。失败时如实报告失败原因，不声称已保存。
- 报告中仅在回测成功后输出快捷入口和真实报告的绝对路径。

## 恢复

- `总结 恢复` 先读取 `{项目根目录}/.transfers/latest.md` 指针，再读取指向的任务报告；使用 `python scripts/inspect_handoff.py {项目根目录}` 比对项目根目录、当前分支和 HEAD。任一不匹配时标为“过期参考”，不得直接继续执行。
- schema=1 旧报告只能标为“旧格式，未验证”；不自动迁移、不覆盖、不把它当作可安全接手状态。
- 文件不存在、项目根目录不明或读取受限时，说明原因并停止；不要创建占位文件。

## 旧版数据

`harvests/`、`_counters.md`、`error-ledger.md`、`_pending.json` 与 `_degradation.json` 是旧版遗留数据。本版本不自动读取、写入、迁移或删除它们。需要处理旧数据时，先由用户明确指定文件和操作。
