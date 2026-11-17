# DESIGN.md — xiaoyaoclaw-agent-orchestrator 设计文档

> 项目：OpenClaw Agent Orchestrator（Agent 协作编排）
> 日期：2026-08-30 | 状态：设计定稿（指挥官逐项拍板）

## 1. 定位

OpenClaw 多 Agent 日常协作编排 skill：把「拆任务 → 分 agent → 管进度 → 聚结果 → 失败重试」
封装成标准工作流，让多个常驻 agent 像团队一样协作。

七件套定位：**协作层**——架在六件套（家/内容/状态/知识/健康/输入）之上，
任何技能都可能需要多 agent 协作。不与六件套并排行列，是横切层。

**不做**（边界）：
- ❌ 不做代码工程编排（compound-eng 红海：swarms/code-review/worktree）
- ❌ 不重写编排引擎（依赖 OpenClaw 原生 sessions 工具）
- ❌ 不做 GUI/可视化监控（openclaw-office 已有）
- ❌ 不做 agent 间消息协议（agentcouch 地盘）

## 2. 竞品结论（2026-08-30 全量扫描）

**ClawHub 2400 技能扫描**：多 agent 编排只有 compound-eng 系列（4 个），全部来自
EveryInc compound-engineering 插件移植（Claude Code 生态），清一色**代码工程场景**：
- compound-eng-orchestrating-swarms（并行 + pipeline 工作流）
- compound-eng-code-review（多 agent 深度代码审查）
- compound-eng-git-worktree（并行开发隔离）
- compound-eng-planning/brainstorming/compound-docs（工程流程配套）

**框架级**（非 skill）：metaswarm（405★）/ orchestrator-supaconductor（375★）/
openclaw-office（640★）/ cc-harness-skills（234★）——均为 Claude Code 编码编排。

**结论**：**OpenClaw 日常协作编排（任务分发/结果汇总/进度管理/失败重试）零竞品**。
Anthropic 官方 19 技能亦零协作类。空白带真实存在。

## 3. 用户故事

1. **多 agent 家庭用户**：我有多个 agent（绘图/调研/编码），想让它们并行干活、自动汇总，一条指令完成
2. **被配置劝退的新手**：跨 agent 通道要改两层配置、allow 要双向——技能自动检测/引导
3. **并行调研场景**：一个主题拆 3 份，3 个 agent 并行查，结果自动聚合一份报告（带来源）
4. **怕超时焦虑的用户**：sessions_send 60s 超时 ≠ 失败——技能轮询查真实状态
5. **失败处理**：某 agent 失败自动重试（≤3 次）/ 3 次失败上报用户
6. **结果溯源**：聚合报告带「哪条结论来自哪个 agent」

## 4. 核心决策（指挥官逐项拍板，2026-08-30）

| # | 决策 | 理由 |
|---|------|------|
| D1 | **强制 sessions_send**（唯一通信路径） | 一劳永逸：对方常驻会话 = 完整人格+记忆+技能；砍 spawn 降级分支，设计简化 |
| D2 | 触发三档：显式直接执行 / 模糊大任务建议+询问 / 默认沉默 | 吸收 tracker v1 全局钩子教训（2026-08-25 下架），技能从不主动抢活 |
| D3 | **直接读 openclaw.json**（agents.list + agentToAgent.allow） | 真相源只有一个，不搞探测中间层；配置不满足时先询问用户，同意后 config.patch（多 agent 共享配置，禁 apply） |
| D4 | Agent 名单 = 直接读 agents.list（砍 agent-roster） | 技能要给别人用，不写死任何环境信息；roster 冗余（名单已在 openclaw.json，能力标签无人维护） |
| D5 | 重试默认最多 3 次（可配置 RETRY_MAX） | 指挥官拍板：默认 3，3 次失败上报 |
| D6 | 进度追踪用 OpenClaw 已有机制 | 同步等待 = sessions_send server-side wait（零实现）；并行 = fire-and-forget + sessions_list/history 查询；不造监听引擎，不用 hooks（网关层，无法驱动会话内逻辑） |

## 5. 编排流程（8 步）

```
① 触发判定    三档：点名/编排动词→直接进；模糊大任务→问一句→确认进；其他→单 agent
② 配置检查    读 openclaw.json：agents.list + allow 双向白名单；未通过→询问用户→同意后 config.patch 补齐（禁 apply），或给指引用户手动改后重试
③ 编排规划    拆子任务（目标 agent + 指令 + 预期产出）→ 展示计划 → 用户确认（可配置 auto 跳过）
④ 并行分发    for 每个子任务: sessions_send(agent, task, timeoutSeconds=0)  ← 即发即返
⑤ 进度追踪    while 未完成: sessions_list/history 查状态 → 判定 完成/在跑/失败
⑥ 结果聚合    收集回复 → 结构化汇总（每 agent 一段 + 来源标注）
⑦ 失败重试    失败判定 → 重新 send（带上次上下文）→ 最多 3 轮 → 仍败则上报
⑧ 交付        汇总报告 + 产出位置 + 来源 → 发给用户
```

**串行依赖任务**（可选路径）：sessions_send(timeoutSeconds>0) 直接同步等，零实现。

## 6. 关键规则

| 规则 | 内容 |
|------|------|
| R1 并行投递 | 所有子任务 timeoutSeconds=0 即发即返，绝不串行等；总时长 ≈ 最慢任务 |
| R2 完成判定 | ✅ [DONE] 结尾（指令模板约定）/ ⏳ 在跑（有中间输出）/ ❌ 失败（明确报错/超时无产出） |
| R3 超时语义 | sessions_send 60s 超时 ≠ 失败——任务后台继续，用 sessions_list/history 确认 |
| R4 重试带上下文 | 重发指令 = 原指令 + 失败原因 + 「避免重复已完成部分」 |
| R5 防 ping-pong | 指令模板内置「收到即执行，一次回复，不要追问」+ maxPingPongTurns 上限双保险 |

## 7. 触发词设计（SKILL.md description）

- 触发：编排 / 并行 / 分给 / 让 XX 做 / 汇总 / orchestrate / parallel / delegate / coordinate
- 建议询问：调研 / 分析 / 巡检 / 审查 / 看看（大而模糊任务）
- 沉默：单 agent 日常问答、简单操作

## 8. 目录结构（目标）

```
xiaoyaoclaw-agent-orchestrator/
├── SKILL.md                  # 主技能（三档触发 + 8 步流程 + 规则 + 双平台命令）
├── manifest.json             # compat: openclaw; category: Collaboration / Orchestration
├── README.md / README.en.md  # 双语（对齐六件套结构：hero + 场景 + 快速开始 + 配置指引）
├── LICENSE                   # MIT
├── PROGRESS.md               # 项目进度卡
├── .gitignore
├── docs/
│   └── DESIGN.md             # 本文档
├── scripts/
│   ├── check_config.py       # 检测 openclaw.json：agents.list + allow 双向白名单 → 状态报告
│   └── check_status.py       # 解析 sessions_list 输出 → 子任务状态汇总（零 token 确定性操作）
├── references/
│   ├── sessions_send.md      # sessions_send 机制详解（超时语义/announce/ping-pong/防坑）
│   ├── agent_to_agent.md     # agentToAgent 配置指南（visibility/allow 双向/坑）
│   └── config_patch.md       # 配置修改安全规范（config.patch vs apply，多 agent 共享配置）
└── templates/
    └── task_prompt.md        # 分发指令模板（[DONE] 结尾约定 + 防 ping-pong 措辞）
```

## 9. 开发计划

| 里程碑 | 内容 | 状态 |
|--------|------|------|
| M1 | 立项（PROGRESS.md + 记忆日志） | ✅ 2026-08-30 |
| M2 | DESIGN.md（本文档） | ✅ 2026-08-30 |
| M3 | SKILL.md + references + templates | ⏳ |
| M4 | scripts（check_config.py / check_status.py） | ⏳ |
| M5 | 本地实测（真实多 agent 编排测试） | ⏳ |
| M6 | README + README.en + assets | ⏳ |
| M7 | GitHub 发布 + 全局技能同步 | ⏳ |
| M8 | ClawHub 提交（确认制，等指挥官点头） | ⏳ |

## 10. 发布链路（对齐六件套）

1. GitHub：dtsola/xiaoyaoclaw-agent-orchestrator（public, main, MIT, topics×N）
2. 全局技能同步：state/skills/xiaoyaoclaw-agent-orchestrator/
3. 七件套 README 互链（六件套 README 补本项目 + 本项目 README 链六件套）
4. ClawHub：v1.0.0 提交 → pending-publication → **等指挥官确认公开**（确认制铁律）
