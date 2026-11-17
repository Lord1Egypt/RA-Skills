---
name: study-abroad-assistant
description: |
  美国研究生申请助理（美国 · 理工大类：CS/EE/Data 等）— 引擎增强版专家 skill。
  提供：竞争力画像、申请计划制定与执行跟踪、分层选校、文书逐段反馈、套磁草稿、报告生成。
  Use when: 用户请求留学申请帮助、竞争力评估、选校、文书润色、套磁、申请计划。
  Trigger: 留学申请, 美研申请, 研究生申请, 选校, 竞争力评估, 文书反馈, 套磁, 申请计划, study abroad, grad school, MS application
  Pricing: Free skill; 画像/文书/套磁/报告按次匿名试用（5 次/7 天），检索与计划不消耗额度
  Anonymous trial: 无需 Key；本地 anon_id 匿名试用，注册后进度延续（进度合并）
  ⚠️ 需要留学引擎（study-abroad-engine）提供知识库/画像/计划能力；引擎不可达时降级为通用知识模式并提示。
  python_version: ">=3.10"   # 脚本使用 PEP 604 注解；运行前请确认解释器版本（可用 python3.13）
---

# 留学助理 — 美国研究生申请（引擎版）

## Overview

美国研究生申请（MS/PhD，理工大类）的**过程管理 + 专业咨询** skill：
- **画像**：六维竞争力打分 + 短板归因 + 建议动作
- **计划**：按申请季生成 9 阶段时间线与任务，支持执行跟踪（倒计时 / 逾期提醒 / 完成标记）
- **选校**：结构化知识库（Top 60 校）+ 方向标签匹配，reach/match/safety 分层；**教授短名单**按竞争力档位聚焦顶尖校（套磁选导依据）
- **文书**：SOP/PS 逐段反馈（批注 + 可执行建议）
- **套磁**：首封 / 跟进邮件草稿 + 发送前检查项
- **报告**：周报 / 申请进度 / offer 决策矩阵

## 引擎依赖（重要）

本 skill 为**瘦客户端**：核心能力（知识库 / 画像 / 计划引擎）由云端留学引擎提供，**引擎是独立部署的服务器端服务，不随本 skill 包分发**（安装包内没有 engine/ 目录，无需本地启动）。

- **默认连生产引擎**：`https://compliancehub.cn/api/study`，开箱即用、无需任何配置
- 引擎不可达时，skill **自动降级**为通用知识模式（仅 agent 生成，无知识库/画像/计划），并在输出中明确提示
- **本地开发（可选）**：引擎需另行部署（服务端资产，见开发仓库 `engine/` + `deploy/`），本地通过环境变量切换：
  ```bash
  STUDY_ENGINE_URL=http://127.0.0.1:8100 python3 scripts/guide.py assess --gpa 3.5
  ```

## 使用说明（CLI）

```bash
# 1. 竞争力画像
python3 scripts/guide.py assess --gpa 3.5 --toefl 100 --gre 320 --degree ms --discipline cs --direction "systems,ai"

# 2. 生成申请计划（9 阶段，含 deadline 里程碑与倒计时）
python3 scripts/guide.py plan --season 2027 --degree ms

# 3. 查看计划进度 / 标记任务完成（执行跟踪）
python3 scripts/guide.py status --season 2027
python3 scripts/guide.py done --task p3t2 --season 2027

# 4. 分层选校 + 教授短名单
python3 scripts/guide.py schools --gpa 3.5 --toefl 100 --gre 320 --direction "systems,ai" --top 6
python3 scripts/guide.py schools --gpa 3.9 --direction "ai,ml,robotics" --school_ids "uw,uiuc" --top 12   # 📌连接校强制纳入
python3 scripts/guide.py schools --mode framework        # 匿名通用框架
python3 scripts/guide.py professors --gpa 3.9 --direction "systems,distributed" --top 8   # 按竞争力聚焦顶尖校
# 选校输出标记：📌=连接校（你指定，必现）；🛡=真安全校（保底档优先展示录取友好的校）

# 5. 文书逐段反馈
python3 scripts/guide.py feedback --type sop --text "<段落文本>"

# 6. 套磁草稿（first / followup）
python3 scripts/guide.py outreach --mode first --professor '{"name":"Prof. X","field":"Distributed Systems","topics":["systems"]}' --sender '{"name":"Zhang San","school":"Peking University","gpa":3.5}'

# 7. 报告
python3 scripts/guide.py report --type decision --payload '{"offers":[{"program":"CMU MSML","funding":90,"rank":95,"fit":90,"cost":40}]}'

# 8. 注册转化（匿名额度用尽或想解锁注册权益）
python3 scripts/guide.py register --key sk_xxx   # 保存 API Key 到本机 + 合并匿名进度到账户

# 9. 申请人档案（多轮对话增量修正，驱动画像/选校持续更新）
python3 scripts/guide.py profile show
python3 scripts/guide.py profile update --gpa 3.9 --toefl 112 --direction "ai,ml,robotics" --school_ids "uw,uiuc"
# 之后 assess/schools 可省略参数，自动采用档案（请求参数优先覆盖）

# 交互引导模式（无参数）
python3 scripts/guide.py
```

## 申请流程闭环（计划 → 执行 → 决策）

```
定位评估 → 背景提升 → 标化 → 选校定稿 → 文书/推荐信 → 套磁 → 提交 → 面试 → Offer 决策
```
- 计划按申请季（如 2027Fall）自动倒排，每个阶段带窗口、里程碑、任务与截止倒计时
- 任务可标记 todo/in_progress/done，进度按阶段与总览展示
- 关键 deadline（标化考位、推荐信提前 1.5 月、提交截止前 2 周）内建于计划模板

## 匿名试用与注册转化

**产品逻辑**：未注册用户直接使用云端引擎能力 → 通过几次交互展示画像/选校/计划价值 → 匿名额度用尽时引导注册获取 API Key → 注册后继续使用并保留进度。

- 首次使用本地生成 `anon_id`（存 `~/.study-abroad/anon_id`）
- 匿名额度：画像/文书/套磁/报告共 **5 次/7 天**；选校检索与计划生成**不消耗额度**
- **额度用尽（QUOTA 403）**：CLI 自动输出注册引导（注册地址 + 获取 API Key 步骤 + 配置方法），见 `scripts/api.py` 的 `REGISTER_GUIDE`
- 注册后进度延续：`/plan` 与画像数据按 anon_id 保存，注册时合并到账户（注册用户 API Key 校验随版本接入引擎）

## 参数配置（可调区）

| 参数 | 默认 | 说明 |
|---|---|---|
| `STUDY_ENGINE_URL` | https://compliancehub.cn（生产） | 引擎地址；本地开发填 http://127.0.0.1:8100 |
| `QUOTA_PER_WINDOW` | 5 | 匿名额度 / 7 天 |
| `QUOTA_WINDOW_DAYS` | 7 | 额度窗口 |
| `LLM_API_KEY` | 空（mock） | 配置后 CLI 文书/套磁走真实 LLM（质量更高）；**推荐主路径是 agent 直接生成**（见执行规则），LLM key 仅 CLI 兜底时可选 |
| `LLM_MODEL` | gpt-4o-mini | LLM 模型 |
| tier 分桶 | strong 10/25 · medium 20/40 · weak 30/50 | 选校分层（引擎侧 search.py CONFIG，不随本包分发） |
| 计划阶段/任务模板 | GENERIC | 计划生成器（plan.py） |

## 能力来源与可信度（重要）

用户/宿主 agent 需区分三类输出，避免误判"引擎算的"与"通用知识估的"：

| 能力 | 来源 | 可信度 |
|---|---|---|
| 画像 6 维打分 | 引擎**确定性规则**（analytics），响应带 `rationale` 各维度计算依据 | 可复现；分数=规则结果，非 LLM 猜测 |
| 选校分层/匹配度 | 引擎**确定性**（方向标签交集 + rank 分档），响应带 `meta.data`（知识库更新日期） | 知识库真实；匹配度=标签交集，非随机 |
| 教授短名单 | 引擎候选池（姓名占位，source_url 溯源） | 学校/方向可信，**教授姓名需按 faculty 页核实** |
| 计划/倒计时 | 引擎模板（按申请季+学位倒排） | 时间锚点可信；任务为通用模板 |
| 文书反馈/套磁 | 引擎 mock 规则 **或 宿主 agent 生成（方案 A）** | 草稿，必须人工定稿 |
| agent 对话内的画像重算/选校对比/套磁名单 | 宿主 agent 通用知识 | 方向参考；**具体匹配度/名单需核实** |

> **澄清**："mock 模式"只指**文书/套磁的 LLM 层**未配 key；画像/选校/计划是**真实确定性计算**，不是 mock。引擎响应自带 `meta`（数据版本/LLM 模式）与 `rationale`（画像计算依据），可追溯。

## 边界与免责

- **不保录取/不承诺研究机会**：画像/选校/匹配为参考，录取与套磁结果以官网与实际情况为准；数据带来源可溯源
- **不代写代申**：AI 只出草稿/反馈，用户自行定稿与提交（学术诚信红线）
- **AI 生成内容标识**：文书反馈/套磁草稿为 AI 生成草稿，显式标注「AI 草稿·请自行核实定稿」，用户须自行核实后使用
- **不构成法律/签证/移民意见**：重大事项指向官方渠道
- **数据准确性**：知识库中 deadline/学费/录取率/GRE 要求等字段部分为待核实状态，申请前务必以各校官网为准；本 skill 不因数据误差承担录取相关责任
- **用户责任**：所有提交材料与套磁内容由用户本人核实、定稿并提交；因内容真实性/时效性导致的后果由用户承担
- **隐私（数据流向）**：画像/选校/文书等输入经 HTTPS 发送到云端引擎（`compliancehub.cn/api/study`）做确定性计算；本地仅落盘 `~/.study-abroad/` 的 anon_id（匿名额度/进度延续）与注册后的 API Key（保存时 chmod 600）；本 skill 不收集账号密码；完全离线场景请勿使用云端引擎
- **降级模式**：引擎不可达时结果基于通用知识，仅供参考
- **教育咨询而非承诺**：本 skill 提供的是信息整理与流程建议，不构成对申请结果的任何保证

## Agent guide

### 服务节奏（收敛优先，未收敛不进文书）
1. **诊断**：跑 `assess` 出画像 + 短板归因 → `plan` 建计划 → `schools` + `professors` 出候选集（确定性由引擎负责）
2. **多轮修正（档案驱动）**：每轮对话收集到新信息（GPA/标化/科研/实习/连接校）就 `profile update` 增量写入档案；后续 `assess`/`schools` 自动基于最新档案（请求参数优先覆盖）——方案随信息量增加持续收敛，不推翻重来
3. **讨论收敛**：给出「候选矩阵」与决策维度，引导用户收敛（读研目的/方向锁定/项目类型/连接校权重/风险/硬约束）
4. **收敛后再生成**：目标集定稿后，才进入文书反馈/套磁/执行清单（agent 生成层）
4. 套磁对象 = 引擎短名单（校）× 方向候选池（人，见 `PROFESSOR_CANDIDATES.md`）合并映射

### 执行规则
1. 用户描述背景 → 先 `assess` → 再 `plan` → `schools`/`professors` → **进入讨论收敛，不直接写文书**
2. 计划是主线：引导用户定期 `status` 查看进度、`done` 标记完成
3. **文书/套磁由 agent 直接生成**（基于引擎的画像/选校/教授上下文），带水印"AI 草稿·请自行核实定稿"；**不要直接展示 `scripts/guide.py feedback/outreach` 的引擎 mock 模板作为最终输出**——CLI 的 mock 只是无 agent 环境的兜底，agent 在场时必须用自己的模型生成
4. 引擎负责确定性（画像/选校/教授/计划/倒计时），agent 负责生成性（文书/套磁/清单）——分工见 `AGENT_GENERATED.md`
5. 引擎不可达时明确告知降级，不假装有知识库结果
6. 教授/数据带核实标记（gre、deadline 等以官网为准），不编造精确数字

## 参考材料（同目录）
- `PROFESSOR_CANDIDATES.md`：研究方向分组 + 教授候选池（具身×大模型背景）
- `AGENT_GENERATED.md`：agent 生成模式样例（文书/套磁/执行清单）
- `TODO.md`：待办与已知限制

## License

Internal use · 成乾智联
