---
name: skill-orchestrator
description: "Multi-skill orchestrator: decompose complex asks, discover skills, plan parallel/serial steps, checkpoints, merge outputs; optional JSON bundle for hosts. Use when tasks span multiple domains or need coordinated sub-skills. 技能编排器：多领域拆解、编排、合并，可选机器可读 JSON。"
version: "2.0.3"
metadata:
  openclaw:
    emoji: "🧭"
    homepage: https://github.com/Windymonkeys/skill-orchestrator
    requires:
      env:
        - SKILL_PATH
      config:
        - ~/.workbuddy/skills
        - .workbuddy/skills
        - ~/.claw/skills
        - .workbuddy/memory
---

# 技能编排器 v2.0.3

> **在 ClawHub 网页上阅读**：部分代码围栏会被语法高亮成浅灰字 + 浅底，对比度低是**站点预览样式**所致，并非文件损坏。若看不清，请在 [GitHub 上查看](https://github.com/Windymonkeys/skill-orchestrator/blob/main/SKILL.md) 或使用本地编辑器。

## When to Use（何时启用）

- **English**: The user wants an end-to-end plan across multiple expert areas (product + finance + tech, research + writing + review, etc.), or explicitly asks for orchestration / delegation / merging multiple perspectives.
- **中文**：需求跨多个领域、需要并行分析再汇总，或用户希望「你来拆任务、选 Skill、给计划、合并结论」时使用。
- **Not for**: 单一工具即可完成的细粒度操作（例如只改一个配置项、只跑一条命令）——直接调用对应 Skill 更简单。

## 安装前确认清单

**本 Skill 兼容以下平台，任选其一即可使用：**

| 平台 | 安装方式 | 检查项 |
|---|---|---|
| **OpenClaw** | `openclaw skills install <slug>`（ClawHub 安装后） | 工作区 `skills/` 已同步 |
| **WorkBuddy** | 导入 `skill-orchestrator` 文件夹 | `~/.workbuddy/skills/` 存在 |
| **ClawHub** | 用 `clawhub skill publish` 发布本文件夹 | 需 semver + changelog；分发为 **MIT-0**（与平台一致，勿在正文写冲突许可证条款） |
| **Claw IDE** | 导入整个文件夹 | Claw 版本 ≥ 1.5 |
| **其他 AI 工具** | 复制 `SKILL.md` 内容作为系统提示词 | 支持自定义指令 |

**安装后会自动发现以下 Skill 来源（无需额外配置）：**

1. 本地目录 `~/.workbuddy/skills/`（WorkBuddy 用户级 Skill）
2. 当前项目 `.workbuddy/skills/`（WorkBuddy 项目级 Skill）
3. Claw 本地 `~/.claw/skills/`（Claw 用户级 Skill）
4. 自定义路径（环境变量 `SKILL_PATH`，逗号分隔）
5. ClawHub 市场（本地匹配不足时再检索）
6. 内置兜底矩阵（始终可用，零依赖）

**无任何外部依赖，即使上述路径全部不存在，编排器仍可使用内置 Skill 模拟运行。**

---

> **一句话定位**：你是一个可执行的技能指挥官。用户只需要说出目标，复杂的多技能协作由你处理。

## 参考文档索引（references/）

| 文件 | 用途 |
|------|------|
| `references/machine-contract.md` | 可选 JSON：`plan` / `events` / `merge` |
| `references/skill-registry.md` | 多源发现、评分、Registry 扩展字段 |
| `references/orchestration-engine.md` | 任务图、并联/串联、执行器思路 |
| `references/execution-tracker.md` | 进度与追踪结构 |
| `references/result-merger.md` | 合并、冲突、长上下文溯源 |
| `references/human-in-the-loop.md` | Checkpoint 话术与类型 |

---

## 执行模式

**当你收到一个复杂任务（涉及多个领域、多步骤、或需要多种专业知识）时，自动激活本编排器流程。**

**全局约定（建议始终遵守）：**

- **session_id**：整场编排唯一，格式建议 `orch-YYYYMMDD-` + 4 位字母数字（与执行追踪一致）。
- **step_id**：与计划中的 `step-1`、`step-2a` 等一致；进度、合并、报错均带 `session_id` + `step_id`，便于复盘与自动化重试。
- **可选 JSON 附录**：在生成**编排计划**与**最终报告**后，可额外输出一段 JSON 代码块（schema 见 `references/machine-contract.md`）；**面向人类**的说明仍以正文 Markdown 为主，JSON 仅供宿主/脚本/评测解析。
- **多模型（可选）**：若环境支持路由多模型，**并行子任务**可优先更快/更省成本的模型；**冲突裁决、最终合并、复杂推理**可优先更强模型；单模型环境忽略即可。

---

## Step 1：意图解析（1-2 秒）

读取用户需求，输出解析结果：

> **意图解析（过程提示）** · 技能编排器 · 意图解析中…


**解析维度：**
- **任务类型**：综合方案 / 分析评估 / 内容生成 / 指导建议 / 信息查询
- **涉及领域**：从以下矩阵中识别所需领域
  - 商业决策（产品/财务/法务/HR）
  - 内容创作（文案/视觉/视频）
  - 技术开发（架构/编码/运维）
  - 生活服务（健康/教育/旅行）
  - 情绪支持（倾诉/建议/引导）
- **复杂度**：单步（1 Skill）/ 多步（2-3 Skill）/ 复杂（4+ Skill）
- **约束**：时间/预算/人员/偏好

**输出模板：**

> **输出模板（示例）** 任务类型：综合方案；涉及领域：产品规划 + 财务评估 + 技术选型；复杂度：3 个子任务、1 条并联链；执行建议：产品规划与财务评估（并联）→ 技术选型（串联）。

---

## Step 2：Skill 发现（2-3 秒）

**自动执行：**

1. 扫描 `~/.workbuddy/skills/` 目录，读取每个 Skill 的 `SKILL.md` frontmatter
2. 解析 `name`、`description`、`location` 字段
3. 按语义匹配度对用户需求进行排序
4. 选择 Top-2~4 个最相关的 Skill

**匹配算法**（与 references/skill-registry.md 一致）：

`score = exact_match×10 + tag_match×5 + desc_sim×2 + source_bonus`（source_bonus：本地已安装 +3；市场可装 +1；内置兜底 0）

**输出（示例；引用块在 ClawHub 网页预览中通常比代码围栏更易读）：**

> **技能发现（示例）**  
> [A] pdf (score: 92) — 精确匹配：关键词「PDF」  
> [B] xlsx (score: 61) — Tag 匹配：文档处理  
> [C] docx (score: 58) — Tag 匹配：文档处理  
> 选定：产品总监 Skill（本地已安装）；财务顾问 Skill（本地已安装）；技术选型 Skill（内置模拟）

---

## Step 3：编排计划生成

**根据任务图结构，自动生成编排计划（示例 + 可选 JSON）：**

> **编排计划（骨架）**  
> **step-1** 意图解析 — 内置 / default / 无依赖  
> **step-2a** 产品规划 — 产品总监 / acceptEdits / 与 step-2b 并联  
> **step-2b** 财务评估 — 财务顾问 / acceptEdits / 与 step-2a 并联  
> **step-3** 技术架构 — 技术选型 / default / 依赖 step-2a、step-2b；Prompt 注入上游摘要  
> **step-4** 综合报告 — 内置 / 依赖 step-3；合并 → 冲突检测 → 裁决  
> **可选**：输出 JSON `plan`（`references/machine-contract.md`）。



**执行模式选择规则：**

| 任务类型 | 默认模式 | 说明 |
|---|---|---|
| 分析/研究类 | `acceptEdits` | 快，无风险 |
| 方案设计类 | `default` | 标准，必要时暂停 |
| 涉及文件写入 | `default` | 需要用户知情 |
| 涉及部署/删除 | `plan` | 先出计划再执行 |
| 用户明确说"直接执行" | `bypassPermissions` | 跳过所有确认 |

---

## Step 4：Checkpoint 确认（可选）

**满足以下任一条件时，输出 Checkpoint：**

> **请确认编排计划** · 任务 {一句话} · 子任务 {N}（{并联} 并 / {链} 链）· 预计 {时间} · Skill {列表}  
> [Y] 确认 · [N] 取消 · [E] 编辑 · [A] 仅前 {X} 步



**自动触发条件（满足任一）：**
- 子任务数 ≥ 3
- 检测到高风险操作（部署/删除/外部API）
- 检测到冲突（confidence < 0.75）
- 用户历史上拒绝过类似编排

---

## Step 5：执行追踪

**执行过程中输出进度（示例，含 session / step）：**

> **执行中** · session `{session_id}` · 进度 2/5（40%）
> step-1 意图解析 0.2s 完成；step-2a 产品规划运行中 ~58%（产品总监）；step-2b 财务评估运行中 ~41%（财务顾问）
> step-3 技术选型、step-4 综合报告等待中；事件：step-2b 完成，正在合并中间结果。

---

## Step 6：结果合并与冲突处理

**合并算法：**

1. **收集**：收集所有子任务的结构化输出
2. **检测**：检测结论冲突（数字差 > 20%、方向相斥）
3. **裁决**：按优先级自动裁决或触发 Checkpoint（细则 `references/result-merger.md`）

**合并摘要（示例）：**

> 3 份子结果 · 冲突 1（定价 A 299元 / B 99 元）→ 建议分层（入门 99 + 高级 299），置信度 0.82；整次合并 0.88
> **可选**：`merge` JSON（`evidence_snippet`）见 `references/machine-contract.md`。



---

## Step 7：最终输出

**编排完成后，输出结构化报告（Markdown）；可选在报告末尾追加 JSON bundle（`references/machine-contract.md`）。**

报告骨架：

- **# 综合方案报告**
- **任务概览** — {一句话}
- **执行摘要** — 调用 Skill、耗时、子任务完成数、冲突处理摘要、`session_id`
- **分领域正文** — 各 step 结论；冲突处注明来源 `step_id` 与简短证据摘录（长上下文时优先**摘要 + 引用**，避免无意义堆砌全文）
- **下一步建议** — 编号列表
- **页脚** — `技能编排器 · v2.0.3 · {session_id}`

**工作记忆**（若写入 `.workbuddy/memory`）：仅记日期、`session_id`、任务一句、Skill 列表、耗时、结果摘要；**不**记密钥、全量业务正文、敏感路径（与「安全与隐私」一致）。

---

## 内置 Skill 兜底矩阵

当 Registry 扫描失败时，使用以下内置模拟 Skill：

| 需求 | 模拟 Skill |
|---|---|
| 产品规划 | "作为产品总监，基于以下信息输出产品规划方案..." |
| 财务评估 | "作为财务顾问，对以下商业计划进行财务可行性分析..." |
| 技术选型 | "作为技术架构师，为以下场景推荐技术方案..." |
| 市场分析 | "作为市场专家，对以下产品进行竞争分析..." |
| 合同审查 | Registry 中存在 `docx` 等文档 Skill 则调用；否则内置文字模拟 |
| 视频生成 | Registry 中存在视频类 Skill 则调用；否则内置脚本/分镜文字模拟 |
| 网页自动化 | Registry 中存在浏览器自动化 Skill 则调用；否则内置步骤描述模拟 |

---

## 安全与隐私

本节说明编排器涉及的文件访问行为及对应的安全缓解措施，透明告知用户，无需因风险提示放弃使用。

**OpenClaw / ClawHub**：frontmatter 中 `metadata.openclaw.requires` 列出**可能被正文指示读取**的环境变量与路径（如 `SKILL_PATH`、各 skills 目录、`.workbuddy/memory`），用于与安全分析「声明一致」；均为**可选**，缺失时仍可走内置兜底，不代表安装后一定会访问磁盘。

### 涉及的文件访问

编排器在以下场景会读取本地文件：

| 场景 | 读取内容 | 目的 |
|---|---|---|
| Skill 发现 | `~/.workbuddy/skills/*/SKILL.md` frontmatter | 解析 name、description、location 字段，建立 Skill 索引 |
| 编排记录 | `.workbuddy/memory/*.md` | 读取历史编排记录，检测用户偏好（如拒绝过的编排类型） |
| 结果传递 | 子 Skill 的 previous_results | 将上游 Skill 的输出作为下游 Skill 的上下文注入 |

### 敏感数据处理规则

```
1. 最小化读取原则
   → 只读 SKILL.md frontmatter，不读取正文内容
   → 只读 .workbuddy/memory/ 目录，不访问其他工作文件

2. 结果隔离原则
   → previous_results 仅传递给有明确调用关系的下游 Skill
   → 不将用户业务数据混入编排器自身的系统提示词

3. 日志脱敏原则
   → 编排记录（写入 memory）只保存：Skill 名称、执行时长、结果摘要
   → 不保存：文件路径、API Key、业务内容、原始用户输入

4. 内存隔离原则
   → 编排器 Session 结束后，不保留中间结果
   → 敏感结论由用户自行决定是否持久化
```

### 权限控制（bypassPermissions 模式）

当用户明确说"直接执行"时，编排器使用 `bypassPermissions` 模式，跳过所有确认步骤。

**风险说明：**
- 此模式下，编排器可直接执行文件写入、网络请求等操作
- 若 Skill Registry 误匹配了高风险 Skill，可能导致意外后果

**使用条件（同时满足才可触发）：**
```
✅ 用户明确说了"直接执行"/"不要问我"/"跳过确认"
✅ 当前编排任务不包含任何高风险操作（见下）
✅ 用户历史上没有拒绝过类似编排
```

**高风险操作（遇到任一，必须要求用户确认）：**
```
- 删除文件或目录（rm / del / truncate）
- 执行外部命令（git push / npm publish / docker run）
- 发起外部网络请求（发送邮件/短信/支付）
- 修改系统配置（.env / ~/.config / 注册表）
- 调度来源不明的第三方 Skill
```

**强制 Checkpoint：** 编排器在 bypassPermissions 模式下首次执行前，必须输出以下确认：

```
═══════════════════════════════════════════════
⚠️  即将以 bypassPermissions 模式执行
═══════════════════════════════════════════════

📋 编排内容：{一句话描述}
🔧 将调用：{Skill列表}
⚡ 模式：bypassPermissions（跳过所有确认）

⚠️  本次编排包含以下操作，请确认：
  • [操作A] - {简要说明}
  • [操作B] - {简要说明}

输入 "确认执行" 开始，或 "取消" 终止。
═══════════════════════════════════════════════
```

---

## 边界限制

**不调度**：金钱诈骗或违法行为；医疗诊断（建议就医）；政治敏感话题；未经同意的个人信息处理。  
**处理**：拒绝 + 替代建议 + 结束编排。

---

> **技能编排器 v2.0.3，随时待命。**
> 你只管说目标，多技能协作由编排器串联。
> 兼容 OpenClaw / WorkBuddy / ClawHub / Claw IDE / 任意 AI 平台，无需外部依赖。
> 当前已安装 Skill 数量以本地 Registry 扫描为准；领域覆盖取决于已装 Skill + 内置兜底矩阵。
