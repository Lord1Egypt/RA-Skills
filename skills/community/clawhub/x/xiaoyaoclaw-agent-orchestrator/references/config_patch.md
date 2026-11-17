# 配置修改安全规范（config.patch vs config.apply）

> 本文档沉淀自多 agent 共享配置的血泪教训（2026-08-13 确立铁律）。

## 1. 背景

多 agent 共享同一份 openclaw.json（所有 agent 定义都在 `agents.list` 里），
互相覆盖风险高。编排技能需要引导用户改配置时，必须遵守本规范。

## 2. 铁律

| 操作 | 允许？ | 原因 |
|------|--------|------|
| `config.patch`（部分合并，只动指定字段） | ✅ **唯一允许** | 安全合并，不影响其他 agent 的修改 |
| `config.apply`（全量替换） | ❌ **禁止** | 用自己会话的旧配置快照整份写回，抹掉其他 agent 的修改 |
| 直接编辑 openclaw.json 文件 | ⚠️ 用户手动可以 | 技能不直接写文件（误写风险 + 无校验） |

## 3. 正确姿势（引导用户）

编排技能遇到白名单缺失时，**先询问用户，用户同意后执行 config.patch**（或输出指引让用户手动执行）：

```bash
# 示例：开启跨 agent 通道（tiantong 编排 xiaoguang）
# 通过 OpenClaw 的 config.patch 接口（或 CLI），只动三个字段：
# 1. tools.sessions.visibility = "all"
# 2. tools.agentToAgent.enabled = true
# 3. tools.agentToAgent.allow = ["tiantong", "xiaoguang"]  ← 双向
```

改完网关重启 ~10s 生效，期间新任务报 GatewayDrainingError 属正常。

> ⚠️ 修改配置是编排的前提：配置不满足时，技能应询问用户「是否帮你补配置？」——用户同意后执行 config.patch；用户拒绝则输出指引，由用户手动处理。

## 4. 为什么不能 apply（背景）

- 7+ 个 agent 共享单份 openclaw.json，apply = 谁后写谁赢
- openclaw.json.bak* 备份就是 apply 全量写入留下的痕迹（事故现场）
- 例外：仅初始化 / 整体迁移等场景才考虑 apply（用户自行决策）

## 5. 技能边界声明

- ✅ 读配置：直接读 openclaw.json（只读）
- ✅ 改配置：**先询问用户，用户同意后**执行 config.patch（只动指定字段，禁 apply）
- ✅ 给指引：用户拒绝时输出 config.patch 修改建议 + 命令
- ❌ 不擅自改配置：未经用户同意不执行任何配置写入
- ❌ 重启网关：不自动重启（影响所有 agent，决策权在用户）
