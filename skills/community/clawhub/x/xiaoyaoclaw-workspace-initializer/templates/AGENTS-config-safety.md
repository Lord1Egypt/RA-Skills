## 配置修改规范（多 agent 共享配置安全）

> 本段是**待用户批准的提议文本**：把它写进 `AGENTS.md` 会改变未来会话的配置操作方式，因此需先给 diff、经用户同意再落地。

多 agent 共享同一份 openclaw.json（所有 agent 定义都在 agents.list 里），互相覆盖风险高：

- ✅ 改配置一律用 gateway `config.patch`（部分合并，只动指定字段）
- ❌ **任何情况下都不使用** gateway `config.apply`（全量替换：会用自己会话的旧配置快照整份写回，抹掉其他 agent 的修改）——包括初始化、迁移、重置等场景；需要大范围变更时，逐字段 `config.patch`，并先展示 diff 等用户确认
- 背景：多个 agent 共享单份 openclaw.json，apply = 谁后写谁赢；openclaw.json.bak* 备份就是 apply 全量写入留下的痕迹
