---
type: project
status: archived
progress: 100
created: 2026-08-30
updated: 2026-09-01
docs:
  - path: SKILL.md
    desc: 技能定义（七件套协作层）
  - path: README.md / README.en.md
    desc: 中英双语文档
  - path: docs/DESIGN.md
    desc: 设计文档（含竞品分析）
  - path: manifest.json
    desc: ClawHub 发布清单
---

# xiaoyaoclaw-agent-orchestrator

> 七件套「协作层」——OpenClaw 多 Agent 日常协作编排

## 状态

**status: archived（已发布，进入维护期）**——2026-08-30 立项并设计定稿 → 2026-08-30 开发与本地实测通过、GitHub 发布 → 2026-09-01 ClawHub v1.0.1 公开（显示名 OpenClaw Cross-Tool Commander 同批收官），九件套互链闭环完成

## 项目定位

- **英文名**：OpenClaw Agent Orchestrator
- **中文名**：Agent 协作编排
- **slug**：xiaoyaoclaw-agent-orchestrator
- **定位**：七件套「协作层」——架在六件套之上，任何技能都可能需要多 agent 协作
- **一句话**：把「拆任务→分 agent→管进度→聚结果→失败重试」封装成标准工作流

## 设计定稿（2026-08-30 指挥官逐项拍板）

### 核心决策
1. **通信路径**：强制 sessions_send（唯一路径，一劳永逸）——对方常驻会话，完整人格+记忆+技能；spawn 降级分支已砍
2. **触发机制**：三档——显式指定直接执行 / 模糊大任务建议+询问 / 默认沉默（吸收 tracker 全局钩子教训）
3. **配置读取**：直接读 openclaw.json（agents.list + agentToAgent.allow），不搞探测；配置不满足时**先询问用户，同意后 config.patch**（多 agent 共享配置，禁 apply）
4. **Agent 名单**：直接读 agents.list（**2026-08-30 砍掉 agent-roster**——名单已在 openclaw.json，能力标签无人维护即冗余），不写死任何环境信息
5. **重试**：默认最多 3 次，可配置；3 次失败上报用户
6. **进度追踪**：主 agent 维护，用 OpenClaw 已有机制——同步等待（server-side wait）串行依赖任务；fire-and-forget + sessions_list/history 并行任务；不造监听引擎，不用 hooks

### 编排流程（8 步）
① 触发判定 → ② 配置检查（双向白名单）→ ③ 编排规划（子任务+agent 匹配+计划确认）→ ④ 并行分发（timeoutSeconds=0 即发即返）→ ⑤ 进度追踪（list/history 判定）→ ⑥ 结果聚合（带来源）→ ⑦ 失败重试（≤3，带上下文）→ ⑧ 交付（汇总+产出位置）

### 关键规则
- 并行投递统一轮询（不串行等）
- 完成判定：[DONE] 结尾 / 在跑（有中间输出）/ 失败（报错/超时无产出）
- 60s 超时 ≠ 失败（任务后台继续）
- 重试带上下文（原指令+失败原因+避免重复）
- 防 ping-pong：指令模板内置「一次回复即完成」

### 目录结构
```
xiaoyaoclaw-agent-orchestrator/
├── SKILL.md / README.md / README.en.md / LICENSE / manifest.json / PROGRESS.md / .gitignore
├── docs/DESIGN.md
├── scripts/check_config.py + check_status.py
├── references/sessions_send.md + agent_to_agent.md + config_patch.md
└── templates/task_prompt.md（agent_roster.md 已移除）
```

## 开发计划

- [ ] M1: 立项完成（PROGRESS.md + 记忆日志）✅
- [ ] M2: docs/DESIGN.md（设计文档，含竞品分析）✅
- [ ] M3: SKILL.md + references + templates ✅
- [ ] M4: scripts（check_config.py / check_status.py）✅ 本地实测通过
- [ ] M5: 本地实测（真实多 agent 编排测试）✅ 全链路通过（send→执行→[DONE] 回复）
- [ ] M6: README + README.en + assets ✅ hero.svg 渲染验证通过
- [ ] M7: GitHub 发布 + 全局技能同步 ✅（repo 1e402e4，topics×8，哈希 MATCH，六项目 README 互链推送）
- [x] M8: ClawHub 提交 ✅ v1.0.1 已公开（2026-09-01 收官）

## 竞品结论（2026-08-30 调研）

- ClawHub 2400 技能扫描：多 agent 编排只有 compound-eng 系列（代码工程场景，EveryInc 移植）
- 框架级：metaswarm/orchestrator-supaconductor（Claude Code 编码编排）
- **空白带：OpenClaw 日常协作编排（任务分发/汇总/进度/重试）零竞品**
- Anthropic 官方 19 技能零协作类
