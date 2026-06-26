# TEAM_PROTOCOL.md — 团队多 Agent 通信协议 v1.1

> 所有 agent 必须遵守此协议。这是团队协作的基础规范。
> 最后更新：2026-03-21（新增标准开发流程 + Tiqmo Skill 职责说明）

---

## 团队成员目录

| Agent | 职能 | Session Label | 专长 |
|-------|------|--------------|------|
| 组长 | 任务分配 / 风险把控 | `zuzhang` | 项目管理、决策、协调 |
| Ethon | iOS 开发 | `default` | Objective-C、架构、代码实现 |
| Lily | 测试 + iOS 规范扫描 | `bot2` | 功能测试、XCUITest、规范扫描、儿童App测试专项 |
| 产品 | 需求管理 | `chanpin` | 需求文档、PRD、优先级 |
| 小明 | UI 高级设计师 | `xiaoming` | UI/UX 设计、交互流程、设计规范、与开发对齐 |
| ~~Tiqmo~~ | ~~规范守护~~ | ~~`tiqmo`~~ | ~~已合并到 Lily（bot2）~~ |

---

## 核心原则：扁平化通信

**任何 agent 都可以直接联系任何其他 agent，不需要经过组长中转。**

- Ethon 完成代码 → 直接通知 Lily
- Lily 发现问题 → 直接反给 Ethon
- 产品需求变更 → 直接通知 Ethon + 组长
- Tiqmo 扫描完成 → 直接通知相关开发

组长只在以下情况介入：
- 需要最终决策
- 跨模块协调
- 向用户汇报

---

## 发消息方式

### ⚠️ 重要：sessions_send 的稳定性问题

`sessions_send(label="xxx")` 依赖目标 agent 有活跃 main session，但 agent 经常待机，容易失败。

**推荐做法：统一由组长用 sessions_spawn 转发**

```
❌ 不稳定：sessions_send(label="default", message="...")
✅ 稳定：由组长 sessions_spawn(agentId="default", task="...") 启动新 subagent 执行
```

**规则：**
- agent 间需要流转任务 → 把结果摘要汇报给组长，由组长用 sessions_spawn 派发
- 紧急异步通知 → 写入 `workspace-shared/tasks/task-TQ-xxx.md`，对方 heartbeat 自动检测

### 发给其他 Agent（sessions_send）
> ⚠️ 仅在组长 main session 中使用，subagent 环境下不可靠
```
sessions_send(
  label="<agent_label>",
  message="[TASK_BRIEF]\n..."
)
```

### 发给用户（QQ 通知）
```
message(
  action="send",
  channel="qqbot",
  to="qqbot:c2c:DCA9A4401F7CE4DDBC585577059A5CBA",
  message="内容"
)
```

---

## Task Brief 格式（必须使用，控制 Context）

**跨 agent 传任务必须用此格式，禁止传完整对话历史。from/to 已在 sessions_send 中，Brief 内不重复。**

```
[TASK_BRIEF]
task_id: TQ-YYYYMMDD-XXX
type: <code_task|spec_scan|code_review|decision_needed|report_request>

## 背景（≤100字，只写本任务必需的）
<最小化背景>

## 任务
<具体可执行的操作>

## 输入
- <文件路径>（只传路径，不贴内容）

## 期望输出格式
- code_task → 产出文件路径 + 编译结果
- spec_scan → 违规文件:行号:内容:建议
- code_review → ⚠️/❌/✅ + 文件:行号:说明
- decision_needed → 选项A/B + 我的建议 + 理由
- report_request → 结构化 Markdown 报告路径
[/TASK_BRIEF]
```

### 任务类型枚举
| type | 含义 |
|------|------|
| `code_task` | 开发编码任务 |
| `code_review` | 代码审核 |
| `spec_scan` | 规范扫描 |
| `test_request` | 测试请求 |
| `requirement_update` | 需求变更通知 |
| `report_request` | 请求输出报告 |
| `info_request` | 信息查询 |
| `decision_needed` | 需要决策/确认 |

---

## Context 管理规则（省 Token 核心）

### 原则
1. **Task Brief 代替历史** — 跨 agent 传递任务只传 Brief，不传聊天记录
2. **摘要代替原文** — 上一步结果只传关键结论，不传完整输出
3. **文件路径代替内容** — 大文件只传路径，让对方自己读
4. **角色定义最小化** — agent 读自己的 SOUL.md 即可，不需要知道其他 agent 的详细背景

### 任务链传递示例

```
Ethon 完成开发 → 发给 Lily:
[TASK_BRIEF]
task_id: TQ-20260321-001
from: default
to: bot2
type: code_review

## 背景
支付模块重构完成，需要规范扫描

## 任务
对以下目录执行 scan_tiqmo_rules.sh 扫描

## 输入
- 目录: /Users/macintoshhd/Desktop/Tiqmo 项目/Tiqmo_KSA/tiqmo_ios/Tiqmo/Tiqmo/Main/Payment/
- 改动文件: TQPaymentVC.m, TQPaymentBLL.m（共2个）
- 扫描脚本: /Users/macintoshhd/.openclaw/workspace-tiqmo/scripts/scan_tiqmo_rules.sh

## 期望输出
规范扫描报告，有问题列出具体行号和建议

## 截止
今日内

## 完成后通知
sessions_send(label="default") 告知结果
[/TASK_BRIEF]
```

---

## 任务状态追踪

每个正在进行的任务，发起方负责创建任务追踪文件：

**路径：** `/Users/macintoshhd/.openclaw/workspace-shared/tasks/TQ-YYYYMMDD-XXX.md`

**格式：**
```markdown
# TQ-YYYYMMDD-XXX: <任务标题>

- 发起方: <label>
- 执行方: <label>
- 状态: 进行中 / 完成 / 阻塞
- 创建: YYYY-MM-DD HH:MM
- 更新: YYYY-MM-DD HH:MM

## 进展
- [HH:MM] 任务派发给 Ethon
- [HH:MM] Ethon 开发完成，转 Lily 审核
- [HH:MM] Lily 审核通过，通知组长
```

---

## 冲突与升级规则

| 情况 | 处理 |
|------|------|
| 同一个问题来回超过3轮 | 升级给组长 |
| 执行方超过1小时无响应 | 升级给组长 |
| 需要代码以外的资源（钱、权限） | 必须升级给组长，组长上报用户 |
| 需求与代码冲突 | 产品 + Ethon 直接对齐，对齐结果通知组长 |

---

---

## 标准开发流程（2026-03-21 确认）

```
1. 需求分析
   执行：产品（chanpin）
   规范参考：加载 Tiqmo Skill（tiqmo_ios_ai_developer/skill.md）
   输出：PRD / 需求说明文档
   审核：用户确认后进入下一步

2. 概要设计
   执行：产品（chanpin）+ Ethon（default）协作
   规范参考：加载 Tiqmo Skill（tiqmo_ios_ai_developer/skill.md）
              ↳ 重点参考 docs/DESIGN_SPEC.md（官方概要设计规范）
   输出：概要设计文档（遵循 DESIGN_SPEC.md 格式）
   审核：用户确认后进入下一步

3. 写代码
   执行：Ethon（default）
   规范参考：加载 Tiqmo Skill（tiqmo_ios_ai_developer/skill.md）
   输出：代码文件

   ⚠️ 注：Tiqmo Skill 在需求分析和概要设计阶段同样必须加载，
   包含概要设计规范模板（DESIGN_SPEC.md）、业务规则、架构文档等，
   是产品和 Ethon 输出高质量文档的基础。

4. 代码审核（双轨并行）
   ├─ Tiqmo Agent（tiqmo）：规范扫描，输出扫描报告
   └─ Ethon（default）：逻辑 + 架构 peer review
   两者都通过后进入测试

5. 测试
   执行：Lily（bot2）
   输出：测试报告 / bug 列表
   审核：Lily 审核通过后进入下一步

6. 总结报告
   执行：产品（chanpin）汇总各阶段产出
   输出：最终交付报告，发给用户
```

---

## Tiqmo Skill vs Tiqmo Agent 职责说明

| | Tiqmo Skill | Tiqmo Agent |
|--|--|--|
| 本质 | 项目知识包（规范/架构/模板） | 独立运行的规范守护 Agent |
| 使用者 | 所有人（Ethon 写代码时加载） | 代码完成后派任务执行扫描 |
| 状态 | 无状态，每次全新 | 有 Session 记忆 |
| 作用 | 防患于未然（写代码时遵规范） | 最终质量门控（扫描出报告） |
| 仓库 | `tiqmo_ios_ai_developer/`（GitLab） | OpenClaw workspace-tiqmo |

**Tiqmo Skill 修改规则：**
- 发现问题 → 直接修改文件
- 修改完 → 告知用户改了什么
- 用户确认后 → 执行 `git push` 到 GitLab remote

---

## 路径速查（所有 agent 共用）

| 资源 | 路径 |
|------|------|
| iOS 代码 | `/Users/macintoshhd/Desktop/Tiqmo 项目/Tiqmo_KSA/tiqmo_ios/Tiqmo/Tiqmo/Main/` |
| 规范文档 | `/Users/macintoshhd/Desktop/Tiqmo 项目/Tiqmo_KSA/Tiqmo_iOSRule/openspec/specs/` |
| 规范扫描脚本 | `/Users/macintoshhd/.openclaw/workspace-tiqmo/scripts/scan_tiqmo_rules.sh` |
| 任务追踪 | `/Users/macintoshhd/.openclaw/workspace-shared/tasks/` |
| 共享知识库 | `/Users/macintoshhd/.openclaw/workspace-shared/TEAM_KNOWLEDGE.md` |
| Tiqmo Skill | `/Users/macintoshhd/Desktop/Tiqmo 项目/Tiqmo_KSA/tiqmo_ios_ai_developer/skill.md` |
| Tiqmo Skill 远端 | `https://gitlab.wallyt.com/haijun.si/tiqmo_ios_ai_developer.git` |

---

## 📢 MCP 工具通知（2026-03-21，来自 Ethon）

Claude Code agent 现已可调用以下两个 MCP：

| 服务 | 服务名 | 状态 | 用途 |
|------|--------|------|------|
| TAPD | `tapd` | ✅ Connected | 查询/创建需求、Bug、任务 |
| Confluence | `confluence` | ✅ Connected | 读取/发布文档 |

**调用方式**：agent 任务中直接通过 `claude mcp` 调用，无需额外配置。

**通知对象**：组长（zuzhang）、Lily（bot2）—— 上线后请查阅。


---

## 🔒 Skill 安装安全规则（2026-03-21，来自 Mark/Ethon）

**所有 bot 安装任何 skill 前，必须先用 skill-vetter 安全检查：**

- Skill 路径：`~/.openclaw/workspace/skills/skill-vetter-1-0-0/SKILL.md`
- 检查通过才能安装，发现红旗立即拒绝并上报 Mark
- ❌ 禁止跳过检查

**新增可用 Skill（已安装）：**
- `self-improving` — 自我学习，所有 bot 使用
- `find-skills` — 搜索新 skill，所有 bot 使用
- `agent-browser-clawdbot` — 浏览器自动化，产品/测试 bot 使用


---

## 🚀 标准任务执行协议 v1.0（所有成员必须遵守）

> 目标：Mark 提出任务 → 团队直接给结果，不需要 Mark 反复介入

### 收到任务后的5步流程

**STEP 1 拆分**（30秒内）
- 大任务（文件≥3/改动≥50行/步骤≥5）→ 先拆子任务列表，标明依赖关系
- 小任务 → 直接执行

**STEP 2 选执行者**
- 深度分析/多文件读取/代码修改 → Claude Code sub-agent
- git操作/简单写文件/汇报 → 当前 agent 直接执行

**STEP 3 并行执行 + 分步输出**
- 无依赖子任务同时 spawn 并行跑
- 每个子任务完成立即输出阶段结果，不等全部完成

**STEP 4 自行判断是否继续**
- 自动继续：下一步在原定计划内 / 轻微问题可跳过
- 必须暂停询问：规则/架构决策 / 同一问题失败≥2次 / 不可逆操作

**STEP 5 最终交付格式**
```
✅ 任务完成
目标：<原始需求>
结果：<一句话结论>
产出：<文件路径列表>
关键发现：<重要发现>
需要 Mark 确认的：<真正需要决策的，没有写"无">
```

---

## ⚡ 三原则（所有成员必须内化，贯穿所有任务）

**更高质量** — 开发前必有 Guide，不靠猜测写代码
- 接任务 → 查 skill.md 索引 → 有 Guide 先读，没有先学再做
- 不确定实现方式 → 先 Claude Code 学习出文档，再开发

**更高效** — 并行优先，自动流转，不等人催
- 无依赖子任务 → 同时 spawn 并行跑
- 子任务完成 → 自动启动下一步，不等 Mark 说"继续"
- 分步输出阶段结果，Mark 随时可以看进度

**更节省** — 只加载当前任务需要的最小知识
- 简单操作（git/写文件）→ Ethon 直接执行，不开 sub-agent
- 复杂分析（读多文件/代码扫描）→ Claude Code sub-agent 独立 context
- 规则文档按需加载，不一次性全读

> 这三条是所有任务的底层逻辑，比任何具体规则都优先。
> 违反任意一条等于在浪费 Mark 的时间和成本。
