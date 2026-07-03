# QA 测试用例生成器

> 从需求文档（Markdown / PDF / Word / 图片流程图）自动生成结构化 Excel 测试用例。

[![Version](https://img.shields.io/badge/version-1.1.0-blue)]()
[![Python](https://img.shields.io/badge/python-3.9%2B-brightgreen)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()

---

## 目录

- [概述](#概述)
- [功能特性](#功能特性)
- [快速开始](#快速开始)
- [工作流](#工作流)
- [支持的输入格式](#支持的输入格式)
- [项目结构](#项目结构)
- [最佳实践](#最佳实践)
- [评估体系](#评估体系)
- [版本历史](#版本历史)
- [贡献指南](#贡献指南)

---

## 概述

**qa-testcase-generator** 是一个 AI 驱动的测试用例生成工具，采用五阶段流水线将需求文档转化为结构化的 Excel 测试用例。核心理念是**将需求映射到可验证的测试场景**。

适用场景：
- 产品需求文档（PRD）→ 测试用例
- API 接口文档 → 接口测试用例
- UI 原型图和流程图 → 交互测试用例
- 含多张图表的综合需求文档 → 整合测试用例

---

## 作为 Skill 使用

本项目是一个 **AI AGENT SKILL**，而不仅仅是 Python 脚本集合。当你在 Claude CODE、codex 等 AI 平台或工具中触发此技能时，AI 会自动加载 `SKILL.md` 并按五阶段流程执行。

### 触发方式

在对话中提及以下内容即可自动触发：

> 生成测试用例、编写测试用例、从需求提取测试场景、根据需求文档/设计文档/接口文档/流程图生成测试、需要按业务域分组的测试报告、测试覆盖、测试计划

**示例对话：**

```
用户：我从产品经理那收到一份用户管理系统的需求文档，需要生成测试用例 Excel
→ AI 自动加载 SKILL.md，执行五阶段流程，输出格式化 Excel
```

### 触发后的流程

1. AI 加载 `SKILL.md` 中的五阶段指令
2. 按阶段一至四依次执行（业务域分析 → 需求提取 → 测试设计 → 用例生成）
3. 阶段五调用 `scripts/writer.py` 生成带格式的 Excel
4. 输出到 `output/` 目录

### 不适用场景

此技能**不会**在以下场景触发：
- 生成自动化测试脚本（Selenium / Playwright）
- 执行测试运行
- 搭建测试框架

> 如果你只想手动运行脚本而不使用 AI Skill 模式，参见下方 [快速开始](#快速开始)。

---

## 功能特性

- **五阶段流水线**：业务域分析 → 需求提取与分类 → 测试设计 → 用例生成 → Excel 输出
- **多格式输入**：支持 Markdown、PDF、Word、图片/流程图
- **结构化输出**：带优先级着色（P0红/P1橙/P2绿/P3灰）和模块分隔行的格式化 Excel
- **七种测试类型**：功能测试、安全测试、性能测试、可靠性测试、兼容性测试、状态迁移、接口测试
- **多种设计方法**：场景法、边界分析、等价类划分、状态迁移、判定表、Pairwise
- **异常分类体系**：输入异常、流程异常、环境异常、权限异常、数据异常、状态异常
- **需求可测性检查**：自动标记不可测和有歧义的需求
- **迭代评估 pipeline**：内置完整的基准测试和对比查看器

---

## 快速开始

### 环境要求

- Python 3.9+
- 依赖库：

```bash
pip install openpyxl
# 可选依赖（需处理 PDF/Word/图片时）
pip install pdfplumber python-docx Pillow
```

### 基本使用

**方式一：从 JSON 直接生成 Excel**

```bash
python scripts/writer.py examples/用户管理系统_测试用例.json
```

**方式二：跟随 SKILL.md 五阶段流程**

1. 将需求文档放入 `tests/` 目录
2. 按照 SKILL.md 的阶段一至五依次执行
3. 在阶段五调用 writer.py 生成 Excel

**方式三：提取外部格式后处理**

```bash
# 提取 PDF 文本
python scripts/extract_pdf.py tests/order_system_v2.pdf -o output/extracted.txt

# 提取 Word 文档
python scripts/extract_docx.py tests/design.docx -o output/extracted.md

# 查看图片元信息
python scripts/extract_images.py tests/flow_chart.png
```

### 输出示例

执行后会在 `output/` 目录生成带格式的 Excel 文件，包含 15 列：序号、用例编号、优先级（颜色标记）、测试维度、用例类型、业务域、设计方法、测试场景、测试点、操作步骤、预期结果、测试数据、前置条件、需求来源、测试结果。

---

## 工作流

### 核心流程

```
阶段一：业务域分析     ═══> output/phase1_domains.json
     ↓
阶段二：需求提取与分类 ═══> output/phase2_requirements.json
     ↓
阶段三：测试设计       ═══> output/phase3_design.json
     ↓
阶段四：用例生成       ═══> output/test_cases.json
     ↓
阶段五：输出 Excel     ═══> output/xxx.xlsx
```

### 各阶段职责

| 阶段 | 输入 | 输出 | 核心活动 |
|------|------|------|----------|
| **阶段一** | 需求文档 | `phase1_domains.json` | 识别业务域、核心实体、状态流转、业务分层 |
| **阶段二** | 需求文档 + 阶段一输出 | `phase2_requirements.json` | 提取需求、复杂度分类、质量属性标记、可测性检查 |
| **阶段三** | 阶段二输出 | `phase3_design.json` | 方法选择、用例策略、质量属性扩展 |
| **阶段四** | 阶段三输出 | `test_cases.json` | 生成每条用例的具体步骤、数据、预期 |
| **阶段五** | 阶段四输出 | 格式化 Excel | 写入 15 列、优先级着色、业务域分隔行 |

### 质量检查清单

详见 `references/quality.md`，涵盖：
- 7 种测试类型覆盖
- 5 种设计方法
- 6 类异常场景
- 覆盖率指标（需求 100%、维度 ≥ 4、方法 ≥ 2）
- 测试数据生成规则（边界值 → 有效等价类 → 无效等价类 → 特殊值）

---

## 支持的输入格式

| 格式 | 提取方式 | 推荐工具 |
|------|----------|----------|
| Markdown (`.md`) | 直接读取分析 | — |
| PDF (`.pdf`) | 文本提取 | `scripts/extract_pdf.py` 或 pdfplumber |
| Word (`.docx`) | 文本+表格提取 | `scripts/extract_docx.py` 或 python-docx |
| 图片/流程图 (`.png/.jpg`) | AI 视觉分析 | 结合 `references/image_analysis.md` |
| API 接口文档 (`.md`) | 结构化解析 | 直接读取 |

---

## 项目结构

```
qa-testcase-generator/
├── SKILL.md                          # 核心技能指令（五阶段流程）
├── evals/
│   └── evals.json                    # 评估用例集（7 eval, 74 断言）
├── scripts/
│   ├── writer.py                     # Excel 生成引擎
│   ├── extract_pdf.py                # PDF 文本提取
│   ├── extract_docx.py               # Word 文档提取
│   ├── extract_images.py             # 图片元信息提取
│   ├── pairwise.py                   # Pairwise 测试组合生成
│   └── generate_test_data.py         # 测试数据生成工具
├── references/
│   ├── quality.md                    # 质量检查清单与生成规则
│   ├── design_methods.md             # 测试设计方法详解
│   ├── schemas.md                    # 评估体系 Schema 文档
│   ├── image_analysis.md             # 图片/流程图处理策略
│   ├── templates.md                  # 用例模板参考
│   ├── environment.md                # 环境配置说明
│   └── troubleshooting.md            # 常见问题排查
├── agents/
│   ├── grader.md                     # 评分代理指令
│   └── analyzer.md                   # 基准分析指令
├── tests/
│   ├── test_requirements.md          # Eval 1: 用户管理系统需求
│   ├── order_system_v2.pdf           # Eval 2: 电商订单系统 PDF
│   ├── design.docx                   # Eval 3: 后台 RBAC 文档
│   ├── login_mockup.png              # Eval 4: 登录 UI 原型图
│   ├── flow_chart.png                # Eval 4: 注册→下单流程图
│   ├── api_docs.md                   # Eval 5: 12 接口 API 文档
│   ├── ecommerce_system.md           # Eval 6: 综合电商需求（含3图）
│   └── conflicting_reqs.md           # Eval 7: 4 处需求冲突文档
├── examples/
│   └── 用户管理系统_测试用例.json      # 完整示例（36条用例，6 业务域）
├── eval-viewer/
│   └── generate_review.py            # 评估查看器生成器
├── docs/
│   ├── iteration2-report.md          # Iteration 2 Benchmark 报告
│   └── iteration2-benchmark.json     # Iteration 2 Benchmark 数据
└── output/                           # 生成输出（.gitignore 忽略）
```

---

## 最佳实践

### 需求文档准备

- 使用清晰的章节结构，每个功能模块独立成节
- 为每个需求分配唯一 ID（如 `REQ-USER-001`）
- 明确标注业务规则、状态流转、边界值
- 避免模糊描述（"良好的用户体验"→ 不可测）

### 测试设计建议

- 每个业务域至少覆盖 **输入 + 流程 + 权限** 三类异常
- 使用 ≥ 2 种设计方法组合（场景法 + 边界分析 + 状态迁移）
- 每条用例 3-5 步操作步骤，提供具体测试数据
- 预期结果避免单独使用"成功"、"正常"等模糊表述

---

## 评估体系

项目内置完整的评估 pipeline，用于量化技能质量：

```bash
# 从 evals.json 生成评估数据
python scripts/run_eval_pipeline.py

# 生成交互式评估查看器
python eval-viewer/generate_review.py workspace/iteration-N \
  --skill-name "qa-testcase-generator" \
  --benchmark workspace/iteration-N/benchmark.json \
  --static workspace/iteration-N/review.html
```

### 评估指标

| 指标 | 说明 | 当前值 |
|------|------|--------|
| Eval 场景 | 覆盖的输入类型 | 7 个（MD/PDF/Word/图片/API/多图/冲突） |
| 断言总数 | 可量化的质量检查点 | 74 条 |
| With Skill 通过率 | 按 SKILL.md 生成的通过率 | 89.1% |
| Baseline 通过率 | 无方法论指导的通过率 | 50.0% |

---

## 版本历史

| 版本 | 日期 | 变更说明 |
|------|------|----------|
| V1.1.0 | 2026-06-29 | 重构评估体系：74 条断言 + 3 个提取脚本 + 阶段独立输出 + 迭代 pipeline |
| V1.0.1 | 2026-06-29 | 拆分质量清单和设计方法至 references/，增加阶段独立输出 |
| V1.0.0 | 2026-06-27 | 初始版本：五阶段工作流、中文字段、Excel输出 |

---

## 贡献指南

1. 在 `evals/evals.json` 中添加新的 eval 场景
2. 在 `tests/` 中准备对应的测试输入文件
3. 运行 `python scripts/run_eval_pipeline.py` 生成 benchmark
4. 通过 `eval-viewer/generate_review.py` 查看评估结果
5. 提交 PR 时附带 iteration benchmark 变化数据

---

## 许可

MIT License — 详见项目 LICENSE 文件。
