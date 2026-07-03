# 错误账本 v3.0 — 全局

> 跨项目、跨会话的**全局**错误频率追踪。每次 `/总结` 自动更新。
> 项目特定错误 → `harvests/{project}/errors.md`
> 同一错误类型出现 3+ 次时高亮标记 ⚠️⚠️⚠️。

## 字段规范

| 字段 | 说明 |
|------|------|
| `错误类型` | 简短描述 |
| `次数` | 累计触发次数 |
| `分类` | PROC/ASSU/ENVR/TOOL/KNOW |
| `涉实体` | 关联的工具/文件/信号 (TOOL:{工具}/SIG:{错误码}/FILE:{后缀}/PROJ:{项目}) |
| `首次` | 首次出现日期 |
| `最近` | 最近出现日期 |
| `days_clean` | 自上次后连续未再犯天数 |
| `避免规则` | 对应规则ID（必须与 AGENTS.md error_patterns 一致） |
| `已验证` | 规则是否回测通过 |

---

## 5 维根因分类体系

| 分类 | 代码 | 定义 | 典型信号 |
|------|:--:|------|---------|
| 流程违规 | PROC | 未遵守现有规则/流程 | Edit前未Read、未验证就说完成、跳过必须步骤 |
| 假设错误 | ASSU | 基于错误假设行动 | 编造API/路径、假设配置存在、未确认前提 |
| 环境问题 | ENVR | 外部环境/工具限制 | 网络被墙、命令不支持、权限不足、版本冲突 |
| 工具误用 | TOOL | 选错工具或参数错误 | 用Bash替代Grep、Edit的old_string不匹配、参数格式错 |
| 知识盲区 | KNOW | 缺少领域/项目知识 | 不知道约定、不了解项目结构、缺少上下文 |

---

## 错误统计

> 字段说明:
> - `days_clean`: 自上次出现后连续未再犯天数（正向激励，归零表示复发）
> - `避免规则`: 对应的预防规则 ID，**必须与 AGENTS.md `<error_patterns>` 表的 ID 一致**（如 `P0-改前先读`）
> - `已验证`: 该规则是否经回测确认有效（✅ 已回测通过 / ❌ 未验证 / 🔄 复发待修订）

| 错误类型 | 次数 | 分类 | 涉实体 | 首次 | 最近 | days_clean | 避免规则 | 已验证 | 涉及项目 | 状态 |
|---------|:---:|:--:|--------|------|------|:--------:|---------|:-----:|---------|------|
| 不换思路连续重试 | 4 | PROC | TOOL:Bash | 06-16 | 06-18 | 0 | P0-换路 | 🔄 | ZCode,codex | ⚠️⚠️⚠️ |
| Edit old_string不匹配 | 3 | PROC | TOOL:Edit, FILE:.md | 06-16 | 06-16 | 2 | P0-改前先读 | ✅ | ZCode | ⚠️⚠️⚠️ |
| Read被harness拦截 | 3 | ENVR | TOOL:Read | 06-16 | 06-16 | 2 | P1-关键读取降级 | ❌ | ZCode | ⚠️⚠️⚠️ |
| PowerShell变量/编码问题 | 2 | TOOL | TOOL:Bash, SIG:编码 | 06-16 | 06-18 | 0 | P1-PowerShell变量 | ❌ | ZCode | ⚠️ |
| 没查协议就写mock | 1 | ASSU | TOOL:Write | 06-17 | 06-17 | 1 | P0-验证后引用 | ❌ | codex | 🆕 |
| 围绕设计行为打补丁 | 1 | PROC | — | 06-17 | 06-17 | 1 | P0-换路 | ❌ | codex | 🆕 |
| 跳过GitHub搜索直接调 | 1 | PROC | TOOL:Grep | 06-17 | 06-17 | 1 | P0-SSH优先 | ❌ | codex | 🆕 |
| GitHub HTTPS推送被墙 | 1 | ENVR | SIG:timeout | 06-17 | 06-17 | 1 | P0-SSH优先 | ✅ | summarize | 🆕 |
| 防火墙block loopback | 1 | ENVR | SIG:denied | 06-17 | 06-17 | 1 | - | ❌ | codex | 🆕 |
| GitHub API空结果 | 1 | TOOL | TOOL:Grep, SIG:timeout | 06-16 | 06-16 | 2 | - | ❌ | ZCode | 🆕 |
| Harness状态不同步 | 1 | ENVR | TOOL:Read | 06-18 | 06-18 | 0 | P1-harness状态 | ❌ | ZCode | 🆕 |
| token暴涨归因误判 | 1 | ASSU | — | 06-22 | 06-22 | 0 | P0-验证后引用 | ❌ | ZCode | 🆕 |
| 长会话context累积未治理 | 1 | KNOW | — | 06-22 | 06-22 | 0 | P0-长会话压缩 | 🔄 | ZCode | 🆕 |
| 研究未调用 agent-reach | 1 | TOOL | TOOL:WebFetch | 06-24 | 06-24 | 0 | P0-技能路由 | ❌ | learn | 🆕 |
| DeepSeek模型名大小写敏感 | 1 | ASSU | — | 06-24 | 06-24 | 0 | P0-验证后引用 | ❌ | ZCodeProject | 🆕 |
| Entity Linking 实现后 error-ledger.md 未同步 | 1 | PROC | TOOL:Edit, FILE:.md | 06-26 | 06-26 | 0 | P0-契约波及清单 | ❌ | summarize | 🆕 |
| _self-stats.md 版本滞后4个里程碑 | 1 | PROC | FILE:_self-stats.md | 06-26 | 06-26 | 0 | P0-契约波及清单 | ❌ | summarize | 🆕 |
| Headroom Rust core 缺失降级为 python_only | 3 | ENVR | TOOL:Headroom SIG:rust_core_missing | 06-21 | 06-21 | 5 | - | ❌ | system | ⚠️⚠️⚠️ |
| Headroom 代理 0 token 节省 | 2 | ENVR | TOOL:Headroom FILE:proxy_savings.json | 06-21 | 06-21 | 5 | - | ❌ | system | ⚠️ |
	
---

## 高频警告区（3+ 次）

| 错误类型 | 次数 | days_clean | 建议 |
|---------|:---:|:--------:|------|
| 不换思路连续重试 | 4 | 0 | `P0-换路` 规则已有，但本次复发 🔄，规则需强化 → 加入"第3次失败必须对用户说出受阻原因和替代方案" |
| Edit old_string不匹配 | 3 | 2 | `P0-改前先读` 规则: "Edit前用 Bash type 确认当前文件内容" → 已写入 AGENTS.md |
| Read被harness拦截 | 3 | 2 | `P1-关键读取降级` 规则: "关键读取用 Bash type 作为 Read 的 fallback" → 已写入 AGENTS.md |

---

## 回测状态摘要

> 每次 `/总结` 时更新，追踪规则遵守情况。

| 规则 | 关联错误 | 最近违反 | 干净天数 | 趋势 |
|------|---------|---------|:--------:|:--:|
| `P0-改前先读` | Edit old_string不匹配 | 06-16 | 6 | ✅ |
| `P0-换路` | 不换思路连续重试 | 06-18 | 4 | ✅ |
| `P0-验证后引用` | token暴涨归因误判 | 06-22 | 0 | 🔄 复发 |
| `P0-SSH优先` | 跳过GitHub搜索 | 06-17 | 5 | ➡️ |
| `P1-harness状态` | Harness状态不同步 | 06-18 | 4 | ✅ 新规则 |
| `P0-长会话压缩` | 长会话context累积 | 06-22 | 0 | 🆕 待验证 |
| `P0-契约波及清单` | error-ledger.md未同步/_self-stats滞后 | 06-26 | 0 | 🆕 新规则 |

---

## 分类分布

| 分类 | 错误数 | 占比 |
|------|:-----:|:--:|
| ENVR 环境问题 | 6 | 32% |
| PROC 流程违规 | 6 | 32% |
| ASSU 假设错误 | 2 | 10% |
| TOOL 工具误用 | 2 | 10% |
| KNOW 知识盲区 | 1 | 5% |
