<p align="center"><b>语言</b>: 中文 · <a href="./README.md">English</a></p>

<p align="center">
  <img src="assets/banner.png" alt="yotta-mirror banner" width="100%" />
</p>

<h1 align="center">元镜 yotta-mirror · 学情分析</h1>

<p align="center">YottaMeta 的<b>确定性学情分析技能</b>：把成绩 / 答题表与题目-知识点映射，变成一份
可复算、可追溯的诊断报告——每条薄弱点结论都带<b>题号、样本量、掌握率与所用阈值</b>。</p>
<p align="center">零依赖（Python 3.8+ 标准库），Windows / Linux / macOS 通用；学生数据只在本机流转，
不联网、不调用模型、不上传。</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue" /></a>
  <a href="https://agentskills.io/"><img alt="Standard: agentskills.io" src="https://img.shields.io/badge/standard-agentskills.io-orange" /></a>
  <a href="https://www.npmjs.com/package/@yottameta/yotta-mirror"><img alt="npm package" src="https://img.shields.io/npm/v/@yottameta/yotta-mirror" /></a>
</p>

## 这是什么

元镜读取结构化成绩表（CSV / TSV / 标准输入）与题目-知识点映射，按固定顺序跑一遍确定性流程：
数据闸门 → 逐题统计 → 按分值加权的知识点掌握率 → 学生分层与临界生 → 带证据的薄弱点诊断 →
Markdown / JSON 报告。

它是教学改进的辅助工具，不是学生评价工具：不产出排名、评语或预测，且每条结论都能用归档输入复算。

## 核心价值

- **结论必带证据**：每条薄弱点给出涉及题号、样本量、掌握率与所用阈值；
- **确定性**：同一份数据与阈值得到同一份报告（仅生成时间不同）；
- **阈值显式**：掌握度、分层、样本量阈值都来自 JSON 配置，并回写进报告；
- **默认人工复核**：低样本统计与分界附近的判断降级为复核项，不硬下结论；
- **隐私优先**：本地运行、不导入网络库、`--anonymize` 产出可分享版本；
- **稳定 JSON 契约**：固定顶层字段，便于自动化、存档与 CI 闸门。

## 快速开始

Windows 使用 `python`，Linux / macOS 使用 `python3`。

```bash
# 1. 生成录入模板（成绩表 + 题目映射 + 阈值配置）
python3 scripts/yotta_mirror.py template --output-dir ./mirror-template

# 2. 分析一次测验，打印 Markdown 报告
python3 scripts/yotta_mirror.py analyze --input scores.csv --items item-map.json

# 3. 输出 JSON，并在薄弱知识点 ≥ 3 时让 CI 失败
python3 scripts/yotta_mirror.py analyze --input scores.csv --items item-map.json \
  --format json --out report.json --gate weak=3

# 4. 匿名化后再分享
python3 scripts/yotta_mirror.py analyze --input scores.csv --items item-map.json --anonymize
```

## 命令一览

| 命令 | 说明 |
|---|---|
| `analyze --input <文件>` | 分析 CSV / TSV 成绩表 |
| `analyze --stdin` | 从标准输入读取成绩表 |
| `analyze --items <文件>` | 题目-知识点映射（必填） |
| `analyze --config <文件>` | 覆盖掌握度 / 分层 / 样本量阈值 |
| `analyze --format md\|json` | 报告格式：Markdown（默认）或 JSON |
| `analyze --out <文件>` | 报告写入文件（默认打印到标准输出） |
| `analyze --anonymize` | 学生标识替换为可复算代号 |
| `analyze --gate weak=<n>` | 薄弱知识点数量达到 n 时退出码 1 |
| `template --output-dir <目录>` | 生成录入门用的成绩表 / 映射 / 阈值模板 |
| `config validate --pack <文件>` | 校验阈值配置 |
| `--version` | 打印引擎版本 |

退出码：`0` 正常 ｜ `1` 触发闸门 ｜ `2` 输入错误 ｜ `3` 配置或映射错误 ｜ `4` 运行时错误。

## 输入格式

```csv
student,T1,T2,T3
S01,5,3,2
S02,5,3,
```

- 第一列 = 学生标识；其余列名 = 题目 id，必须与映射一致；
- 单元格 = 该题得分；留空 = 缺失，报告单独计数；
- 判定题用 `0` / `1`，并在映射里把 `max_score` 设为 `1`。

```json
{
  "schema_version": "1.0",
  "items": [
    {"id": "T1", "max_score": 5, "knowledge": ["有理数运算"], "difficulty": "easy"}
  ]
}
```

完整字段与报错对照见 [references/data-format.md](references/data-format.md)。

## 报告契约

Markdown 结构：输入摘要 → 逐题统计 → 知识点掌握 → 学生分层 → 薄弱点诊断 → 人工复核 → 免责声明。

JSON 顶层字段：`schema_version`、`tool`、`tool_version`、`generated_at`、`input`、`quality`、
`items_stats`、`knowledge`、`layers`、`diagnoses`、`review_items`、`summary`、`thresholds`、`disclaimer`。

字段定义、判定规则与退出码见 [references/report-format.md](references/report-format.md)。

## 数据与隐私

- 学生数据不出本机：引擎不导入网络库、不调用模型；
- `--anonymize` 用 `S-` + 标识 SHA-256 前 8 位替换姓名 / 学号，同一数据集内可复算、跨数据集不可反推；
- 报告固定免责声明：仅用于教学改进，不用于学生评价、排名或升学判断；
- 分享前请加 `--anonymize`，并按学校数据管理规定处理原始成绩表。

细节与安全使用清单见 [references/privacy.md](references/privacy.md)。

## 安装

### 方式一 — npx 一行装（推荐）

```bash
npx -y @yottameta/yotta-mirror --agent codex     # 亦可 --agent claude | cursor | gemini | opencode ...
npx -y @yottameta/yotta-mirror --dir <技能目录>
```

### 方式二 — git clone

```bash
git clone https://github.com/YottaMeta/yotta-mirror.git <技能目录>/yotta-mirror
```

### 方式三 — 下载 ZIP

在 https://github.com/YottaMeta/yotta-mirror 页面点 Code → Download ZIP，解压到智能体的技能目录。

### 方式四 — install.sh

```bash
bash install.sh --list                  # 查看智能体 → 默认目录
bash install.sh --agent codex           # 安装到某个智能体
bash install.sh --dir <技能目录>        # 安装到指定目录
```

## 与家族技能协同

- **元呈 yotta-present**：把学情报告渲染成统一、可复制的格式；
- **元忆 yotta-memory**：按需保存报告摘要与阈值版本；
- **元规 yotta-compliance**：对含学生个人信息的材料做条款级合规审查；
- **元真 yotta-humanize**：面向教师 / 家长的叙述性文字去 AI 味；
- **元阁 yotta-skills**：把「分析 → 呈现 → 记录」编排成一条工作流。

## 运行要求

- Python 3.8+（仅标准库）
- UTF-8 编码的 CSV / TSV 输入；不需要额外依赖、数据库或服务

## 许可证

MIT，见 [LICENSE](LICENSE) 与 [NOTICE](NOTICE)。
