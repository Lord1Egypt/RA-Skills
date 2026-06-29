---
name: thesis-workflow
version: 2.0.0
description: "多Agent协作完成MBA/学术论文写作的完整工作流，支持双版本起草、审核、整合、定稿。"
metadata:
  clawdbot:
    emoji: "📝"
    requires: {}
    os: ["linux", "darwin", "win32"]
---

# MBA/学术论文多Agent协作工作流

> 完整文档见：`references/checklist.md`（学术规范清单）、`references/loop-design.md`（Loop 设计原理）

## ⚠️ 触发规则

当用户请求生成 Word 文档且满足以下任一条件时，**必须**调用本 skill 的 Word 输出流程，不得使用简单 md2docx 脚本：
- 输入文件路径匹配：`论文*.md`、`*thesis*.md`、`*dissertation*.md`
- 上下文中存在「论文」「MBA」「答辩」「开题」等关键词
- 用户明确要求导出 `.docx` 格式且文件性质为学术论文

**正确流程：** 写作语法预检 → Review Agent 终审（`scripts/loop_self_check.py` 校验通过）→ `scripts/md2docx_strict.py` 合规转换 → Word 输出

## 核心架构

```
Phase 1（规划）→ Phase 2（双版本起草）→ Phase 2.5（用户确认）
→ Phase 3（格式审核）→ Phase 3.5（学术深度评审）
→ Phase 4（整合）→ Phase 5（终审）→ [Phase 5.1 去AI味] → Phase 5.2（Word 输出）
```

⚠️ **阶段强制顺序：** 全部 Phase 必须按顺序执行，不得跳过。Phase 2.5（人工确认门槛）和 Phase 3.5（深度评审）是固定节点，不得跳过。

## Agent 设计原则

**每个 Agent 只做一件事。** Agent 间通过文件传递结果，不共享上下文。Orchestrator 专注调度，不执行执行性工作。

| Agent | 调用方式 | 主责 |
|-------|---------|------|
| **Orchestrator** | 当前 session | 调度 / 推进 / 决策 |
| **H-generator** | `exec hermes chat` | 版本H起草（深度逻辑链） |
| **Executor** | `sessions_spawn` | 版本O起草 + 格式执行 |
| **Reviewer** | `sessions_spawn` | Phase 3/5 规则型审核 |
| **DeepReviewer** | `sessions_spawn` | Phase 3.5 学术深度评审 |
| **Integrator** | `sessions_spawn` | Phase 4 整合方案 |
| **WordAgent** | `exec python3` | md2docx执行 + 格式校验 |

## 关键实现说明

### 版本H/版本O 的分工

- **版本H（Hermes优先）：** `hermes --version` 检测安装，可用则 `hermes chat`，不可用回退到 `sessions_spawn` subagent。版本H prompt 必须包含「数据查询工具」说明（`web_search` / `academic-research` / `arxiv-search-collector`），让 Agent 主动搜索行业数据而非仅靠内部知识。
- **版本O（OpenClaw）：** 始终通过 `sessions_spawn` 启动 subagent，格式规范优先。

### 公司信息处理

- 用真实公司名搜索公开数据，填入正文时替换为代号（A公司/B公司）
- 搜索 prompt 用真实名，输出 prompt 用代号
- 映射关系不进入最终文档

### 检索同步规则

所有 Phase 调用数据查询工具（`web_search` / `academic-research`）时，必须：
1. 同步输出工具名称 + 查询条件 + 结果摘要（<50字）
2. Subagent 用 `sessions_send` 向主 session 发送同步
3. 大型检索完成后输出结构化结果摘要

### 数据查询工具

| 工具 | 场景 | 调用 |
|------|------|------|
| `web_search` | 行业数据/市场规模/企业信息 | 直接描述搜索需求 |
| `academic-research` | 学术文献/引用分析 | `python3 scripts/scholar-search.py search "关键词"` |
| `arxiv-search-collector` | 前沿论文追踪 | 初始化后批量抓取 |

## Phase 详解

### Phase 1：规划与定稿

通过问答输出确认清单，用户逐项确认后方可动笔。

**红色星标项（必填）：**
- ⭐ 实际公司名称（仅用于数据检索，正文以A公司/B公司呈现，不进入公开文档）
- ⭐ 大纲结构（7章大纲逐章确认）
- 论文基本信息（题目/作者/专业/学位类型/答辩年份）

→ 生成「写作任务书」用户签收后进入 Phase 2。

### Phase 2：双版本起草

**前置检查：** Phase 1 必填项已确认 / Hermes 可用 / Executor 可用

**章节×版本对照：**

| 章节 | 版本O | 版本H |
|------|-------|-------|
| 第1/2/7章 | ✅ 必须 | ❌ |
| 第3/4/5/6章 | ✅ 必须 | ✅ 必须（核心章节双版本对比） |

**Phase 2 强制检索要求**（关键词中的 `{论文主题行业}` 由 Orchestrator 自动提取）：
- 第3章 PESTEL 分析前 → 搜索「{论文主题行业} 市场规模/趋势/政策」
- 第3章 五力模型分析前 → 搜索「{论文主题行业} 主要竞争对手/市场份额」
- 战略理论部分 → 搜索「{论文主题行业} 竞争战略 应用」
- 每章至少 1 个引用标注来源，全文检索记录 ≥ 3 次

**输出物：** 版本O文件（第1-7章全部）+ 版本H文件（第3-6章全部）
**状态文件机制：** `{论文名}_任务状态.json`（见 `scripts/state_manager.py`）

→ 所有文件存在且字数达标后进入 Phase 2.5（用户确认）。

### Phase 3：双版本审核

Reviewer 分别对版本H和版本O输出独立审核报告。审核维度：格式 / 大纲 / 内容准确性 / 查重风险 / 学术规范 / 写作语法。

### Phase 3.5：深度学术评审（固定节点）

DeepReviewer 对 Phase 3 报告进行二次审查，输出 P0/P1/P2 分级问题清单。P0 问题进入修订 → 重审闭环（见审核 Loop）。

### Phase 4：整合

Integrator 汇总 Phase 3 + Phase 3.5 全部评审结果，制定整合方案。核心原则：取长补短，不为统一而破坏内容质量。

**自动验证：** 整合版运行 `python3 scripts/loop_self_check.py` 校验，100%通过方可输出 Word。

### Phase 5：终审与输出

- Phase 5：Reviewer 终审
- Phase 5.1：[可选] `humanize-chinese` skill 去AI味
- Phase 5.2：`python3 scripts/md2docx_strict.py` 生成 Word 文档

## Orchestrator 生命周期管理

> 执行脚本：`scripts/orchestrator.py`
> 配合 OpenClaw cron 实现自动推进

### 启动方式

用户确认 Phase 1 任务书后，Orchestrator 创建 cron job（每 5 分钟检查一次状态文件）。

```bash
# 手动触发决策（测试用）
python3 scripts/orchestrator.py 论文_xxx_任务状态.json

# 决策 + 自动校验
python3 scripts/orchestrator.py 论文_xxx_任务状态.json --validate
```

### 生命周期

```
用户启动 → 创建 cron（每5分钟检查状态文件）
             ↓
    orchestrator.py 读取状态文件 → 决策引擎判断
    ┌───────────────┬────────────┬───────────────┐
    ↓               ↓            ↓               ↓
  执行下一 Phase   HIL 暂停     RETRY 打回      全部完成
                     ↓            ↓                ↓
                 发消息等你     Agent 补写      cron 删除自己
                 回复确认后     → 恢复循环
                 恢复循环
```

### HIL 节点（自动暂停，需你确认）

| 节点 | 暂停原因 | 确认后行为 |
|------|---------|-----------|
| Phase 1→2 | 公司映射表 + 大纲 | 进入 Phase 2 |
| Phase 2→2.5 | 章节内容是否预期 | 进入 Phase 3 |
| Phase 3.5→4 | P0 修复超 3 轮 | 接受/继续修订 |
| Phase 4→5 | 整合方案是否接受 | 进入终审 |

### 审核 Loop 自动重审

Phase 3.5 完成 → orchestrator 解析 P0 计数 → 有 P0？→ 自动进入修订
→ 修订完成 → 自动回到 Phase 3.5 重审 → 连续 2 轮无新 P0 → 通过
→ 超过 3 轮 → HIL 暂停

### Phase 内部自检

每 Phase 完成后，orchestrator 自动运行 `loop_self_check.py` 校验：
```bash
python3 scripts/orchestrator.py 状态文件.json --validate
```
校验失败 → RETRY 打回 → Agent 修复 → 再次校验（最多 3 次）

## ⚠️ Loop 设计原则

> 详细原理见 `references/loop-design.md`

| Loop 元素 | 作用 | 终止条件 |
|----------|------|---------|
| **Orchestrator Loop** | 每 Phase 完成后自动判断下一步 | 全部 7 Phase 完成 |
| **Phase 内部自检 Loop** | Observe → Think → Act → Verify 四步 | Guardrails 100% 通过 |
| **审核 Loop** | 审→改→重审→连续2轮无新P0→通过 | 连续 2 轮无新 P0/P1 |
| **Guardrails 校验** | `scripts/loop_self_check.py` 10项自动化检查 | 全部通过 |
| **Verification Loop** | Word 输出后自动校验格式 | Word 格式 100% 通过 |

**最大重试：** 每个 Loop 3 次，超过则强制 Human-in-the-loop。
**Human-in-the-loop检查点：** Phase 1/2.5/4/5.2 末尾，必须用户确认才能推进。

## Guardrails 校验（10 项）

```bash
python3 scripts/loop_self_check.py --file 论文_xxx.md   # 单文件
python3 scripts/loop_self_check.py --phase 2 --workspace ~/.openclaw/workspace/  # Phase 级别
python3 scripts/loop_self_check.py --file 论文_xxx.docx --verify-docx           # Word 校验
```

| # | 校验项 | 失败阻断 |
|---|--------|---------|
| 1 | 章节完整性（7章齐全） | Phase 2/4 |
| 2 | 字数门槛（每章≥100行） | Phase 2/4 |
| 3 | 参考文献存在 | Phase 4 |
| 4 | 无 `## 第X章` 混合格式 | Phase 2/4 |
| 5 | 无 `**正文加粗**` | Phase 2/4 |
| 6 | 引用完整性（≥10处） | Phase 2/4 |
| 7 | 三线表列数一致 | Phase 4 |
| 8 | 表标题在表上方 | Phase 4 |
| 9 | 无合并残留（`===END===`） | Phase 4 |
| 10 | 核心章节关键词（第5章战略/第6章实施） | Phase 2.5 |

## Word 输出质量保障

### 正文加粗过滤
- 正文段落（非标题级）内的 `**text**` → 去掉 `**` 转为普通文字
- 表格单元格内的 `**` 同步清除（`scripts/md2docx_strict.py` 的 `_strip_bold()` 函数）

### 三线表格式
- 顶线 1.5 磅 / 表头底线 0.75 磅 / 底线 0.5 磅，无竖线

### 分页
- 每章标题前插入分页符（首章跳过），附录/致谢前分页

## 附录：脚本与文档结构

```
mba-thesis-workflow/
├── SKILL.md                    ← 本文件（简版触发器 + 核心逻辑）
├── README.md / README_EN.md    ← 安装/使用说明
├── CHANGELOG.md                ← 版本日志
├── config.template             ← 配置模板
├── install.sh                  ← 安装脚本
├── .clawhubignore / .github/workflows/skill-publish.yml
├── scripts/
│   ├── md2docx_strict.py       ← Word 合规转换
│   ├── loop_self_check.py      ← Guardrails 自动化校验（10项）
│   ├── state_manager.py        ← 状态文件管理
│   └── tests/                  ← 单元测试
└── references/
    ├── checklist.md            ← 学术规范人工对照清单
    └── loop-design.md          ← Loop 设计原理说明
```
