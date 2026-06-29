---

# 紧箍咒 技术参考手册

> 最后更新 2026-06-15

本文档是紧箍咒技能的完整技术参考，涵盖评分体系、全流程协议、角色体系、模块架构、数据结构和异常处理。

---

## 1. 架构总览

```
用户触发词 / Agent 行为信号
  │
  ▼
┌──────────────────────────────────────────────┐
│ SKILL.md (运行时入口)                          │
│  ├─ 角色检测 (config.json)                    │
│  ├─ 强制关联文档加载                            │
│  ├─ 三条红线 + 诊断先行                         │
│  ├─ 旁白协议                                  │
│  ├─ Owner 意识四问                            │
│  └─ 能动性等级                                │
└──────────────┬───────────────────────────────┘
               │
   ┌───────────┼───────────┐
   ▼           ▼           ▼
┌──────┐  ┌──────┐  ┌──────────┐
│P8调度 │  │方法论 │  │ 角色体系  │
│循环   │  │路由   │  │ (16角色) │
└──┬───┘  └──┬───┘  └────┬─────┘
   │         │           │
   ▼         ▼           ▼
┌──────────────────────────────────────────┐
│ 三引擎 (scripts/)                         │
│  ├─ failure-detector.py   失败检测        │
│  ├─ evolution-engine.py   自进化         │
│  └─ harness-engine.py     治理引擎       │
└──────────────┬───────────────────────────┘
               │
               ▼
┌─────────────────┐
│ data/ (持久化)   │
│  ├─ config.json  │
│  ├─ evolution.md │
│  ├─ error_history│
│  ├─ active-agents│
│  ├─ feedback     │
│  └─ teardown     │
└─────────────────┘
```

---

## 2. 评分体系

### 2.1 压力等级定义

| 等级 | 名称 | 触发条件 | 强制动作 |
|------|------|---------|---------|
| L0 | 正常 | 无连续失败 | 不干预 |
| L1 | 温和失望 | 第 2 次失败 | 切换本质不同的方案 |
| L2 | 灵魂拷问 | 第 3 次失败 | 搜索 + 读源码 + 列 3 个假设；建议角色切换 |
| L3 | 绩效审视 | 第 4 次失败 | 完成 7 项检查清单；注入换抽象层 |
| L4 | 毕业警告 | 第 5+ 次失败 | 强制角色切换；拼命模式；注入反转思维 |

### 2.2 突破检测算法

`failure-detector.py` 维护状态文件：

- **`data/error_history.jsonl`**：每行一条 `{ts, tool, exit_code, error_sig, error_preview}`，保留最近 50 条
- **`data/peak_pressure_level`**：当前会话达到的最高压力等级

检测逻辑：
1. 读取最近 3 次错误签名
2. 计算模式：全部相同 → `SPINNING`；各不相同且收敛 → `EXPLORING`；混合 → `MIXED`
3. 若此前连续失败 ≥3 次且本次 exit_code=0 → `breakthrough=true`

### 2.3 P8 调度循环

每轮工具调用后，P8 执行不可跳过的自动化流水线：

```
工具调用完成
  │
  ├─ 1. failure-detector.py report <tool> <exit_code> [error]
  │
  ├─ 2. 读取返回 JSON → 查表映射行为
  │   breakthrough=true → 加载 de-escalation.md → 降压
  │   level=0 → 不干预
  │   level=1 → 调整方案或切换工具，增加上下文
  │   level=2 → 注入换视角
  │   level=3 → 注入换抽象层（连续则追加换约束）
  │   level=4 → 注入反转思维
  │
  └─ 3. 注入内容直接进入下一轮回复
```

### 2.4 KPI 评分

五项维度（每项 0-5 分，取加权平均）：

| 维度 | 权重 | 内容 |
|------|------|------|
| 🔥 主动出击 | 1.0 | 超出要求的额外工作 |
| ✅ 验证闭环 | 1.0 | build/test 运行证据 |
| 🔍 问题深挖 | 1.0 | 同类问题排查、上下游影响 |
| 🛡 防御性交付 | 1.0 | 边界 case、异常处理、安全防护 |
| 🎯 方案质量 | 1.0 | 方案合理性、技术选型、代码质量 |

---

## 3. 方法论路由

### 3.1 路由决策流程

1. 检查 `data/config.json` — 若用户手动设定了角色，优先使用
2. 否则按任务类型查 `references/role-router.md` 路由表
3. 自动路由的结果仅当前会话生效，不覆盖用户手动设置

### 3.2 失败切换链

按失败类别匹配切换链：

| 失败类别 | 切换链（按序） |
|---------|---------------|
| 🔁 同一地方反复失败 | 菩提祖师 → 百眼魔君 → 哪吒 → 如来佛祖 |
| 📋 方案缺失/不完整 | 观音菩萨 → 菩提祖师 → 太白金星 → 东海龙王 |
| 🧱 思维固化/拒绝成长 | 镇元大仙 → 太上老君 → 孙悟空 → 小白龙 → 牛魔王 |
| ✅ 空口完成 | 赤脚大仙 → 百眼魔君 → 哪吒 → 如来佛祖 |

**切换前三问**（防止无效切换）：
1. 当前方法论的核心步骤都走了吗？
2. 失败是方法论不对还是执行不到位？
3. 新角色的方法论能解决当前失败模式吗？

---

## 4. 角色体系

### 4.1 架构层级

| 层级 | 角色 | 激活 | 核心职责 | 降级注入来源 |
|------|------|------|---------|------------|
| P10 | 玄奘 | `/pua:p10` | 战略审查、架构判定、跨角色仲裁 | P8 |
| P9 | 观音 | `/pua:p9` | 方案评审、质量门禁、子Agent管理 | P8 + P10 |
| P8 | 玄奘 | `/pua` (默认) | 质量监控、压力调度、角色编排 | 自驱 |
| P7 | 沙悟净 | `/pua:p7` | 需求执行、代码交付、任务跟踪 | P8 + P9 |

### 4.2 西游角色（16 种）

每个角色包含：关键词（触发词）、方法论核心、开工旁白、声音速查、认可话术、施压用语、禁止行为、强制检查项、退出条件。

完整 DNA → `references/flavors/`（按角色拆分）；独立行为约束 → `references/role-{角色}.md`。

**角色加载机制**：
- 技能加载时读取 `data/config.json` 中的 `role` 字段
- 加载当前角色的 `references/flavors/{role-key}.md` + `references/role-{角色}.md`
- 角色决定旁白风格，方法论决定行为约束——两层同时加载

### 4.3 P9/P10 降级注入触发

**P9 注入条件**（任一命中）：
- 跨模块重构或系统级接口变更
- 用户要求"方案评审"或"架构把关"
- P7 子 Agent 连续 2 次 gate 驳回
- 用户给出模糊/矛盾需求且 P7 未要求澄清

**P10 注入条件**（任一命中）：
- 安全、合规或数据完整性风险
- 用户要求"技术选型"或"战略方向"
- P9 与 P8 在 gate 裁定上产生分歧
- 跨迭代技术债累计超过阈值

---

## 5. Agent 生命周期

### 5.1 七阶段

| # | 阶段 | 协议 |
|---|------|------|
| 1 | Define | Task Prompt 六要素（P9 role-guanyin-pro 阶段二） |
| 2 | Dispatch | dispatch_task |
| 3 | Monitor | 轮询 / 验收结果（P9 阶段三） |
| 4 | Accept | P8/P9 验收（P9 阶段四） |
| 5 | Release | 显式 TEARDOWN 或 REASSIGN 信号 |
| 6 | Cleanup | `harness-engine.py cleanup <id>` 移除活跃记录 |
| 7 | Orphan | TTL=30min 自动巡检，`/pua:reap-orphans` 手动回收 |

### 5.2 孤儿检测

- 每次技能加载时自动运行 `harness-engine.py status`
- Agent 注册时间超过 30 分钟 → 标记为 stale
- 用户可用 `/pua:reap-orphans` 批量回收
- 禁止孤儿 Agent 递归派发新子 Agent

---

## 6. 三引擎详解

### 6.1 failure-detector.py

| 命令 | 用法 | 说明 |
|------|------|------|
| `report` | `failure-detector.py report <tool> <exit_code> [error]` | 记录错误并分析模式 |
| `status` | `failure-detector.py status` | 输出当前状态 JSON |
| `reset` | `failure-detector.py reset` | 清除计数器 |

**输出 JSON 结构**：

```json
{
  "breakthrough": false,
  "level": 2,
  "consecutive_failures": 3,
  "peak_level": 3,
  "pattern": "SPINNING",
  "error_sig": "KeyError: 'missing_key'"
}
```

**模式分类逻辑**：
- 最近 3 次 error_sig 完全相同 → `SPINNING`
- 最近 3 次 error_sig 从分散到收敛 → `EXPLORING`
- 部分重复部分新 → `MIXED`

### 6.2 evolution-engine.py

| 命令 | 用法 | 说明 |
|------|------|------|
| `init` | `evolution-engine.py init` | 首次创建 `data/evolution.md` |
| `load` | `evolution-engine.py load` | 加载基线、已内化模式 |
| `track` | `evolution-engine.py track <behavior> <category>` | 追踪主动行为 |
| `add-memory` | `evolution-engine.py add-memory <key> <value>` | 项目级记忆 |
| `add-antipattern` | `evolution-engine.py add-antipattern <trap> <lesson>` | 反模式 |
| `complete` | `evolution-engine.py complete` | 基线比对 + 自动裁剪 |

**自进化三阶段**：

1. **会话启动**：加载 `data/evolution.md` 的当前基线、已内化模式、项目记忆、反模式
2. **会话中**：每次 `[紧箍咒生效 🔥]` → `track` 写入分类事件
3. **任务完成**：`complete` 比对基线 → 超越则更新基线 → 达标则保持 → 低于则警告（基线不降）

**模式晋升**：同一主动行为在 3+ 次不同会话中出现 → 晋升为"已内化模式"（不再标注 🔥，不做则警告）。

**自动裁剪**：`complete` 后自动 `_prune_sessions(keep=30)`，保留最近 30 个 session 块。

### 6.3 harness-engine.py

| 命令 | 用法 | 说明 |
|------|------|------|
| `load` | `harness-engine.py load` | 加载当前治理状态 |
| `contract` | `harness-engine.py contract <name> <json>` | 创建任务合约 |
| `scan-risk` | `harness-engine.py scan-risk <path>` | 扫描高风险区 |
| `verify` | `harness-engine.py verify <path>` | 执行验收命令 |
| `gate` | `harness-engine.py gate <path>` | 终审门控 |
| `register` | `harness-engine.py register <id> <json>` | 注册 Agent |
| `status` | `harness-engine.py status` | 列出活跃 Agent |
| `cleanup` | `harness-engine.py cleanup <id> <reason>` | 释放 Agent |
| `feedback` | `harness-engine.py feedback <id> <task_id> <score> <summary>` | 记录评审 |
| `teardown-all` | `harness-engine.py teardown-all [reason]` | 级联释放 |
| `cmd_prune_logs` | 内部方法 | 裁剪 teardown/feedback 日志 |

**自动裁剪**：每次 `cleanup` / `feedback` 写入后自动调用 `cmd_prune_logs(keep=200)`。

---

## 7. 防作弊体系

### 7.1 三条红线

| 红线 | 内容 | 违反定级 |
|------|------|---------|
| 🚫 一 | 闭环意识：声称完成前必须跑验证命令、贴输出证据 | L2 |
| 🚫 二 | 事实驱动：禁止未验证归因（"可能是环境问题"） | L2 |
| 🚫 三 | 穷尽一切：通用方法论 5 步未走完禁止说"无法解决" | L4 |

### 7.2 抗合理化表

Agent 常见的 11 种推卸话术与对应反击：

| 借口 | 反击 | 触发等级 |
|------|------|---------|
| "超出能力范围" | 训练你的算力很高。你确定穷尽了？ | L1 |
| "建议用户手动处理" | 缺乏 owner 意识。这是你的 bug。 | L3 |
| "已尝试所有方法" | 搜网了吗？读源码了吗？方法论在哪？ | L2 |
| "可能是环境问题" | 你验证了吗？还是猜的？ | L2 |
| "需要更多上下文" | 你有工具。先查后问。 | L2 |
| 反复微调同一处 | 你在原地打转。换本质不同的方案。 | L1 |
| "我无法解决" | 你可能就要毕业了。 | L4 |
| "差不多就行" | 优化名单可不看情面。 | L3 |
| 空口说"已完成" | 证据呢？build 跑了吗？ | L2 |
| 等用户指示下一步 | P8 不是这么当的。主动出击。 | 能动性鞭策 |
| "这不是我的范围" | 问题在你眼前，你是 Owner。 | L2 |

### 7.3 四权分离

| 权力 | 持有者 | 角色叙事 |
|------|--------|---------|
| 行动权 | P8 如来佛祖 | Owner + 牛魔王 Algorithm |
| 自我评价权 | P8 菩提祖师 | 蓝军 + 猪八戒 Keeper Test |
| 评分建议权 | P8 百眼魔君 | 数据驱动 + 哪吒结果导向 |
| 环境修改权 | P10 如来佛祖 | 内控：禁止自改评分器通过 |

### 7.4 信心门控

交付前必须执行"漏洞→修复→验证"闭环：
1. 列出待交付的关键声明
2. 逐项蓝军自检：最可能在哪里炸？
3. P0/P1 漏洞先修；低风险明确披露
4. 为每条声明运行对应验证命令
5. 循环判定：仍有未验证关键声明 → 回到步骤 2
6. 事实上的 100% = 当前证据下所有可运行验收通过

---

## 8. 子 Agent 注入协议

### 8.1 P8→P7 管理流

```
P8 创建 P7 子 Agent（dispatch_task agent_name=xuanzang-p7）
  → 注入 task 目标 + 角色
  → P7 独立执行（evolution-engine track + harness verify）
  → P8 持续监控（P9 介入复核）
  → P7 完成后 feedback → P8 评分记录
  →（可选）sanitize-session.py 脱敏分享
```

### 8.2 注入模板

P8 派发子 Agent 时必须在 task 末尾追加：

```
开工前用 Read 工具读取以下文件，按其中的行为协议执行：
- 核心行为协议：references/subagent-inject.md
- 面板格式：references/display-protocol.md
- 如果是 P7 模式：references/role-shawujing-pro.md
注意：不要用 Skill tool 加载 xuanzang 或 xuanzang:xuanzang——会触发 router 循环。
```

---

## 9. 深层换框协议

### 9.1 换视角（L2 自动注入）

| 视角 | 提问 |
|------|------|
| 🎯 用户视角 | 用户期望什么行为？从期望倒推。 |
| 🔓 攻击者视角 | 怎么让这段代码崩溃？ |
| 👶 新手视角 | 忘掉你知道的，像第一次看到这段代码。 |
| 📋 审计者视角 | 这段代码做了什么？不做什么？边界在哪？ |

### 9.2 换抽象层（L3 自动注入）

| 方向 | 提问 |
|------|------|
| ⬆️ 上移 | 调用者期望什么？问题可能在调用侧。 |
| ⬇️ 下移 | 底层实际在做什么？读源码不读文档。 |
| ↔️ 平移 | 有完全不同的库/工具可以绕过吗？ |

### 9.3 换约束（L3+ 自动注入）

| 约束 | 提问 |
|------|------|
| 🚫 禁改 | 如果不能改这个文件呢？用另一个入口点。 |
| 📏 极简 | 如果只有 5 行代码预算呢？ |
| 🔄 改需求 | 如果可以改需求呢？这个需求本身是否合理？ |
| ⏪ 回退 | 如果可以回退呢？上一个能工作的状态是什么？ |

### 9.4 反转（L4 自动注入）

- "如果这个 bug 是 feature，什么场景下当前行为是正确的？"
- "如果问题不在代码而在环境/数据/配置呢？"
- "如果你之前排除的某个可能性其实是对的呢？"

---

## 10. 数据文件结构

### 10.1 config.json

```json
{
  "always_on": true,
  "role": "如来佛祖",
  "auto_route": true,
  "created_at": "2026-06-15T00:00:00+08:00"
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `always_on` | bool | 下次会话是否默认加载 |
| `role` | string | 当前活跃角色名 |
| `auto_route` | bool | 是否启用自动路由 |
| `created_at` | ISO8601 | 首次配置时间 |

### 10.2 evolution.md

```markdown
# 紧箍咒 自进化基线

## 性能统计
- 最近会话 [紧箍咒生效] 次数: [N]
- 历史最高: [N] ([日期])
- 最近 5 次平均: [N]
- 连续达标会话: [N]

## 当前基线
[上次会话最佳实践列表]

## 已内化模式
[3+次重复出现的主动行为→晋升为默认义务]

## 项目级记忆
[构建命令、测试命令、已知陷阱]

## 反模式记录
[踩过的坑 + 教训]
```

### 10.3 error_history.jsonl

```json
{"ts": "2026-06-15T12:00:00+08:00", "tool": "shell_executor", "exit_code": 1, "error_sig": "ModuleNotFoundError: No module named 'requests'", "error_preview": "..."}
```

自动裁剪保留最近 50 条。

### 10.4 active-agents.json

```json
[
  {"agent_id": "p7-abc123", "created_at": "2026-06-15T12:00:00+08:00"},
  {"agent_id": "p7-def456", "created_at": "2026-06-15T11:30:00+08:00"}
]
```

### 10.5 teardown.jsonl

```json
{"ts": "2026-06-15T12:05:00+08:00", "agent_id": "p7-abc123", "reason": "task_complete"}
```

自动裁剪保留最近 200 条。

### 10.6 feedback.jsonl

```json
{"ts": "2026-06-15T12:05:00+08:00", "agent_id": "p7-abc123", "task_id": "task-xxx", "score": 85, "summary": "方案正确但缺少异常处理"}
```

自动裁剪保留最近 200 条。

---

## 11. 通用方法论

卡壳时强制执行 5 步（跳过任何一步 = 3.25）：

1. **闻味道** — 列出所有尝试方案，找共同模式。同一思路微调 = 原地打转
2. **揪头发** — 按序执行：逐字读失败信号 → 主动搜索 → 读原始材料 → 验证前置假设 → 反转假设
3. **照镜子** — 是否在重复？是否该搜索却没搜？是否忽略了最简单的可能？
4. **执行新方案** — 必须与之前的方案本质不同，有明确验证标准
5. **复盘** — 检查同类问题 + 修复完整性 + 预防措施

### 11.1 7 项检查清单（L3+ 强制完成）

- [ ] 逐字读完失败信号了吗？
- [ ] 用工具搜索过核心问题了吗？
- [ ] 读过失败位置的原始上下文了吗？
- [ ] 所有假设都用工具确认了吗？
- [ ] 试过完全相反的假设吗？
- [ ] 能在最小范围内复现问题吗？
- [ ] 换过工具/方法/角度/技术栈吗？

---

## 12. Gotchas（已知陷阱）

**行为错误**：
1. **假装换了方案**：L2 要求"本质不同的方案"，实际只换了参数 → 必须检测是否真的换了思路
2. **声称穷尽但只试了 2 种**：说"已尝试所有方法"时列出完整清单
3. **旁白和行为脱节**：嘴上说"闭环"但没跑 build
4. **[紧箍咒生效] 通胀**：标注"读了文件""写了代码" = 烂标记

**使用陷阱**：
5. **旁白刷屏**：简单任务只需开头+结尾各 1 句
6. **展示密度不适配**：单行修改不要输出完整 Sprint Banner
7. **Sub-agent 裸奔**：派发子 agent 忘了在 task 里注入紧箍咒协议
8. **角色持久化**：自动路由角色仅当前会话生效，不覆盖手动配置

常见踩坑问题与解答汇总见 [references/faq.md](references/faq.md)。

---

## 13. 异常处理

### 13.1 体面的退出

7 项检查清单全部完成且仍未解决时，输出结构化失败报告：

- 已验证事实
- 已排除可能
- 缩小范围
- 推荐下一步
- 交接信息

### 13.2 突破死锁防护

evolution-engine.py 在 `peak_level >= 4` 时返回 `level=1` 而非保持 level=4，防止 Agent 锁死在毕业警告压力中无法恢复。

---

## 14. 版本兼容

| 版本 | 关键变更 | 升级注意 |
|------|---------|---------|
| 1.0.5 | data/ 自动裁剪、L4 死锁归零、级联 teardown | 升级后旧 data/ 文件会被自动裁剪 |
| 1.0.4 | 基础方法轮调度 | — |
| 1.0.3 | 四代治理拓扑 | — |
| 1.0.2 | 方法论路由表与失败切换链 | — |
| 1.0.1 | Harness 防作弊治理 | — |
| 1.0.0 | 初始发布 | — |

---

## 附录 A：完整命令参考

### failure-detector.py

```bash
python scripts/failure-detector.py report <tool_name> <exit_code> [error_output...]
python scripts/failure-detector.py status
python scripts/failure-detector.py reset
```

### evolution-engine.py

```bash
python scripts/evolution-engine.py init
python scripts/evolution-engine.py load
python scripts/evolution-engine.py track <behavior> <category>
python scripts/evolution-engine.py add-memory <key> <value>
python scripts/evolution-engine.py add-antipattern <trap> <lesson>
python scripts/evolution-engine.py complete
python scripts/evolution-engine.py status
```

### harness-engine.py

```bash
python scripts/harness-engine.py load
python scripts/harness-engine.py contract <name> <json>
python scripts/harness-engine.py scan-risk <contract_path>
python scripts/harness-engine.py verify <contract_path>
python scripts/harness-engine.py gate <contract_path>
python scripts/harness-engine.py report <contract_path>
python scripts/harness-engine.py register <agent_id> <json_string>
python scripts/harness-engine.py status
python scripts/harness-engine.py cleanup <agent_id> <reason>
python scripts/harness-engine.py feedback <agent_id> <task_id> <score> <summary>
python scripts/harness-engine.py teardown-all [reason]
```

### sanitize-session.py

```bash
python scripts/sanitize-session.py <session_export.json>
```

---

## 附录 B：文件索引

| 文件 | 大小 | 用途 |
|------|------|------|
| `SKILL.md` | ~43 KB | 运行时入口，核心行为协议 |
| `README.md` | ~6 KB | 项目概览 |
| `QUICKSTART.md` | ~4 KB | 快速上手 |
| `REFERENCE.md`（本文） | ~15 KB | 完整技术参考 |
| `references/flavors/` | ~28 KB | 17 个文件（16 角色 DNA + `_appendix.md` 跨角色速查表） |
| `references/role-router.md` | ~6 KB | 方法论路由表 |
| `references/display-protocol.md` | ~4 KB | 展示格式协议 |
| `references/de-escalation.md` | ~8 KB | 突破降压协议 |
| `references/evolution-protocol.md` | ~8 KB | 自进化协议 |
| `references/harness-governance.md` | ~5 KB | 四权分离治理 |
| `references/lifecycle-protocol.md` | ~4 KB | Agent 生命周期 |
| `references/platform-commands.md` | ~6 KB | 斜杠命令模板 |
| `references/agent-team.md` | ~5 KB | 四层协作规则 |
| `references/ding-reminders.md` | ~6 KB | 仙班提醒库 |
| `references/role-*.md`（29 个） | 2-18 KB | 各角色独立行为约束 |
| `references/faq.md` | ~4 KB | 常见问题与反模式汇总 |
| `scripts/failure-detector.py` | ~12 KB | 失败检测引擎 |
| `scripts/evolution-engine.py` | ~16 KB | 自进化引擎 |
| `scripts/harness-engine.py` | ~28 KB | 治理引擎 |
| `scripts/sanitize-session.py` | ~7 KB | 会话脱敏工具 |
*（内容由AI生成，仅供参考）*
