<div align="center">

<img src="assets/alagent_logo.png" alt="ALAGENT Logo" width="120">

# X2Strategy

**任意研究输入 → 策略规格 → 可执行代码 → 回测 → 诊断报告**

[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue?logo=python&logoColor=white)](https://python.org)
[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-green.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent_Skills-compatible-blueviolet?logo=visualstudiocode)](https://agentskills.io/)
[![Tests](https://img.shields.io/badge/tests-180_passed-brightgreen)]()
[![LiteLLM](https://img.shields.io/badge/LLM-any_provider-orange?logo=openai)](https://docs.litellm.ai/docs/providers)

[快速开始](#-快速开始) · [工作原理](#-工作原理) · [示例](#-示例) · [文档](#-文档) · [English](README.md)

---

*将量化金融研究——论文、草稿、研报或策略想法——自动转化为经过验证的可执行交易策略。*

</div>

## 亮点

- **🔬 多格式输入** — PDF 论文、Markdown 草稿、DOCX 研报、纯文本。自动检测格式。
- **🧠 5 层 LLM 提取** — 多策略检测 → 指标提取 → 信号逻辑 → 执行计划 → 风控规则。
- **✅ 可验证的代码生成** — AST 语法校验 + Backtrader 结构检查 + 指标注册表核查，而非"生成然后祈祷"。
- **📊 自动化回测** — 自动执行回测、提取指标，并与论文报告的结果进行对照诊断。
- **🤖 Agent 原生** — 作为 [Agent Skill](https://agentskills.io/) (`/x2strategy`) 运行在 VS Code Copilot、Claude Code 或任何兼容的 Agent 平台。
- **💰 每篇论文约 ¥0.7** — 推荐使用 DeepSeek，支持任意 [LiteLLM 兼容模型](https://docs.litellm.ai/docs/providers)。

## 工作原理

```
                        ┌──────────────────────────────────────────────────────────────┐
                        │                    X2Strategy                              │
                        │                                                              │
  PDF / MD / DOCX / TXT │   ┌─────────┐   ┌───────────┐   ┌──────────┐   ┌─────────┐ │
  ─────────────────────►│   │  解析    ├──►│  提取      ├──►│  生成    ├──►│  回测   │ │
                        │   │(parser) │   │(L0 → L4)  │   │ (code)   │   │+ 诊断   ││
                        │   └─────────┘   └───────────┘   └──────────┘   └─────────┘ │
                        │        ▼              ▼               ▼             ▼        │
                        │   PaperContent   StrategySpec   Backtrader.py   Report.md   │
                        └──────────────────────────────────────────────────────────────┘
```

| 阶段 | 输入 | 输出 | 说明 |
|:------|:-----|:-----|:-----|
| **解析** | 任意文档 | `PaperContent` | 格式自适应提取（PyMuPDF / 直读 / python-docx） |
| **提取** | PaperContent | `StrategySpec[]` | 5 层 LLM：检测策略 → 提取指标、逻辑、执行、风控 |
| **生成** | StrategySpec | `strategy.py` | 数据模块 → 信号模块 → 回测模块 → 整合 |
| **验证** | strategy.py | 通过 / 失败 | AST 语法 + Backtrader 结构 + 指标存在性检查 |
| **回测** | strategy.py | 绩效指标 | 子进程执行，超时控制，指标提取 |
| **诊断** | 绩效指标 | `report.md` | 与论文报告结果对比，标记偏差 |

## 快速开始

### 方式 A：作为 Agent Skill（推荐）

> [Agent Skills](https://agentskills.io/) 是开放标准。Clone 到 Agent 的 skill 目录后，Agent 自动发现 `SKILL.md` 并注册 `/x2strategy` 斜杠命令。

#### OpenClaw用户 / 安装到OpenClaw

OpenClaw 用户可以直接从 ClawHub 安装：

```bash
openclaw skills install patrick-lew/x2strategy
```

也可以使用 ClawHub CLI：

```bash
npx clawhub@latest install x2strategy
```

如果需要远程或引导式安装，可以将下面的提示词粘贴到 OpenClaw：

```text
Install the skill "X2strategy" (patrick-lew/x2strategy) from ClawHub.
Skill page: https://clawhub.ai/patrick-lew/x2strategy
Keep the work scoped to this skill only.
After install, inspect the skill metadata and help me finish setup.
Use only the metadata you can verify from ClawHub; do not invent missing requirements.
Ask before making any broader environment changes.
```

#### Claude Code/Codex/Copilot 用户 可以将技能直接 clone 到本地 Agent 的技能目录：

<table>
<tr><td><b>GitHub Copilot</b></td><td>

```bash
git clone https://github.com/ALAGENT-HKU/x2strategy.git ~/.copilot/skills/x2strategy
```

</td></tr>
<tr><td><b>Claude Code</b></td><td>

```bash
git clone https://github.com/ALAGENT-HKU/x2strategy.git ~/.claude/skills/x2strategy
```

</td></tr>
<tr><td><b>项目级共享</b></td><td>

```bash
git clone https://github.com/ALAGENT-HKU/x2strategy.git .github/skills/x2strategy
```

</td></tr>
</table>

安装依赖（安装Skill成功后，初始化时Agent会自动完成，也可也手动安装依赖）：

```bash
cd ~/.copilot/skills/x2strategy   # 或你 clone 到的路径
# 如果没有安装uv，请执行 pip install uv
uv sync --extra codegen                  # 核心 + backtrader + yfinance + akshare
```

> [!IMPORTANT]
> 目录名**必须**为 `x2strategy`（与 `SKILL.md` 中的 `name` 字段一致）。安装后，在对话中输入 `/x2strategy` 即可调用，或 Agent 在相关上下文中自动激活。

### 方式 B：独立 CLI 工具

```bash
git clone https://github.com/ALAGENT-HKU/x2strategy.git && cd x2strategy
uv sync --extra codegen    # 核心 + 回测
uv sync --extra agent      # + FAISS 语义搜索（适合 100+ 页的长论文）
uv sync --extra dev        # + pytest
```

<details>
<summary>使用 pip 替代 uv</summary>

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[codegen,agent,dev]"
```

</details>

### 快速上手

```bash
# 1. 配置
cp .env.example .env          # 填入 API Key（推荐 DEEPSEEK_API_KEY）

# 2. 从任意格式文档提取策略规格
uv run python scripts/analyze.py paper.pdf -o library/my_paper/
uv run python scripts/analyze.py strategy_draft.md -o library/my_draft/
uv run python scripts/analyze.py report.docx -o library/my_report/

# 3. 验证已有或生成的 Backtrader 策略文件
uv run python scripts/validate_strategy.py library/my_paper/strategy.py
```

或者直接使用 **Agent Skill** — 只需说：

> *"分析这篇论文并实现其中的主要策略"* + 附上 PDF 文件

Agent 会自动完成全部流程：解析、提取、代码生成、验证、回测和诊断。

## 支持的输入格式

| 格式 | 扩展名 | 解析器 | 说明 |
|:-----|:-------|:-------|:-----|
| **PDF** | `.pdf` | PyMuPDF → Mode A（直接）或 Mode B（FAISS） | 完整支持，覆盖 95%+ 论文 |
| **Markdown** | `.md` `.markdown` | 直接文本读取 | 适合策略草稿、笔记 |
| **Word** | `.docx` | python-docx（`uv sync --extra docx`） | 适合内部研究报告 |
| **纯文本** | `.txt` | 直接读取 | 原始策略描述 |

格式根据文件扩展名自动检测，无需额外配置。

## 示例

[`examples/`](examples/) 目录中提供了真实论文的预生成输出：

| 论文 | 检测到的策略 | 产物 |
|:-----|:------------|:-----|
| **战术资产配置** (Faber 2007) | 1 — GTAA + SMA 择时 | 规格 + 代码 |
| **配对交易** (Goncalves-Pinto et al.) | 3 — 距离法、平稳性、协整 | 规格 |
| **价值与动量** (Asness et al.) | 2 — 价值因子、动量因子 | 规格 |

<details>
<summary>输出目录结构示例</summary>

```
library/tactical_aa/
├── content.json          # 解析后的论文内容
├── content.md            # 可读的论文摘要
├── spec.json             # 结构化策略规格
├── spec.md               # 可读的策略规格
├── metadata.json         # 运行元数据（模型、耗时等）
├── strategy.py           # 生成的 Backtrader 代码
├── validation_report.md  # AST + 结构验证报告
└── results/
    ├── backtest_output.txt
    └── diagnosis_report.md
```

</details>

## 项目结构

```
x2strategy/
├── paper2spec/                 # 阶段 1：文档 → 结构化规格
│   ├── config.py               #   环境变量与 library 路径配置
│   ├── parser.py               #   多格式解析器（PDF / MD / DOCX / TXT）
│   ├── pdf_utils.py            #   PDF 提取辅助函数
│   ├── extractor.py            #   PaperContent → ExtractionResult (L0-L4)
│   ├── models.py               #   数据模型（PaperContent, StrategySpec 等）
│   ├── prompts.py              #   5 层提取 prompt 模板
│   ├── llm.py                  #   LiteLLM 统一接口
│   ├── render.py               #   JSON → Markdown 渲染
│   └── search.py               #   arXiv + SSRN 论文搜索
│
├── spec2code/                  # 阶段 2：规格 → 代码 → 回测 → 诊断
│   ├── validator.py            #   AST + 结构 + 指标验证
│   ├── config.py               #   代码生成与回测配置
│   └── models.py               #   CodeModules, ValidationResult
│
├── references/                 # 经过验证的领域知识（非 LLM 幻觉）
│   ├── backtrader_patterns.md  #   源码验证的 Backtrader 模式
│   ├── indicator_cookbook.md    #   官方指标参数参考（来自 bt 源码）
│   ├── data_sources.md         #   yfinance + akshare API 文档
│   ├── paper2spec.md           #   Paper2Spec 深入指南
│   ├── spec2code.md            #   Spec2Code 深入指南
│   └── skill-internals.md      #   Skill 配置与环境细节
│
├── scripts/                    # CLI 入口
│   ├── analyze.py              #   完整 paper2spec 管线
│   ├── extract.py              #   从解析内容提取规格
│   ├── parse.py                #   将文档解析为 PaperContent
│   ├── search.py               #   搜索论文
│   ├── generate_schemas.py     #   生成 JSON Schema
│   ├── run_full_tests.sh       #   测试运行辅助脚本
│   └── validate_strategy.py    #   独立策略验证
├── schemas/                    # JSON Schema 定义
├── examples/                   # 预生成的参考输出
├── tests/                      # 180+ 单元测试和集成测试
├── SKILL.md                    # Agent Skill 入口
└── pyproject.toml              # 项目配置与依赖
```

## 核心设计决策

<table>
<tr>
<td width="50%">

### 为什么用 Reference Docs 而非 Prompts？

LLM 经常在 Backtrader API 细节上产生幻觉：
- SMA 默认 `period` 是 `30`，而非 `20`
- RSI 内部使用 `SmoothedMovingAverage`，而非 EMA
- BollingerBands 的 line 名是 `.top/.mid/.bot`，而非 `.upper/.lower`

我们的 `references/` 目录包含**经过源码验证**的知识。Agent 按需读取这些文档——在 API 细节上零幻觉。

</td>
<td width="50%">

### 为什么用结构化规格作为中间产物？

直接从论文生成代码会丢失可审计性。`StrategySpec` 中间层的价值：
1. **可审计** — 人工可以在代码生成前审阅规格
2. **可复用** — 同一规格可以适配不同回测引擎
3. **可测试** — 规格提取和代码生成可以独立验证

</td>
</tr>
</table>

## 配置

| 环境变量 | 默认值 | 说明 |
|:---------|:-------|:-----|
| `PAPER2SPEC_LIBRARY_PATH` | `./library` | 输出根目录 |
| `PAPER2SPEC_MODEL` | `openai/gpt-4o-mini` | LLM 模型（[LiteLLM 格式](https://docs.litellm.ai/docs/providers)） |
| `SPEC2CODE_BACKTEST_TIMEOUT` | `300` | 回测超时（秒） |
| `DEEPSEEK_API_KEY` | — | DeepSeek（推荐：最佳性价比） |
| `OPENROUTER_API_KEY` | — | OpenRouter（一个 Key 访问所有模型） |
| `OPENAI_API_KEY` | — | OpenAI 直连 |

所有脚本支持 `--model` 参数覆盖 `PAPER2SPEC_MODEL`。

## 文档

| 资源 | 说明 |
|:-----|:-----|
| [SKILL.md](SKILL.md) | Agent Skill 指令——路由、配置、交互门控 |
| [references/paper2spec.md](references/paper2spec.md) | Paper → Spec 提取深入指南 |
| [references/spec2code.md](references/spec2code.md) | Spec → Code 生成深入指南 |
| [references/backtrader_patterns.md](references/backtrader_patterns.md) | 源码验证的 Backtrader 模式 |
| [references/indicator_cookbook.md](references/indicator_cookbook.md) | 官方指标参数参考 |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | 管线架构 |

## 测试

```bash
pytest tests/ -v              # 180+ 确定性测试
pytest tests/ -v --run-real   # + 真实 API 测试（需要 DEEPSEEK_API_KEY）
```

## 路线图

- [ ] 多引擎支持（Zipline, VectorBT）
- [ ] PDF 中的表格与公式提取
- [ ] 批量处理模式（多篇论文并行）
- [ ] [qsa-benchmark](https://github.com/ALAGENT-HKU) 集成（50 篇论文回归基准）
- [ ] 统一 `StrategySpec` 标准 schema（对接 QSA 平台）

## 参与贡献

欢迎贡献！请参阅[架构文档](docs/ARCHITECTURE.md)了解代码库。

```bash
git clone https://github.com/ALAGENT-HKU/x2strategy.git && cd x2strategy
uv sync --all-extras
cp .env.example .env  # 填入 API Key
pytest tests/ -v      # 验证所有测试通过
```

## 许可证

[Apache-2.0](LICENSE) · 由 **[ALAGENT AI 优彦智能](http://home.alagent.cloud)** 构建 — 可验证、可信赖的金融 AI

---

<div align="center">

## 💬 加入社区

<a href="https://home.alagent.cloud">🌐 官网</a> &nbsp;·&nbsp; <a href="https://github.com/ALAGENT-HKU">GitHub</a> &nbsp;·&nbsp; <a href="mailto:contact@alagent.cloud">📧 contact@alagent.cloud</a>

<br>

<img src="assets/wechat_QR.jpg" alt="微信交流群二维码" width="260">

**扫码加入 ALAGENT 开源交流群**

</div>
