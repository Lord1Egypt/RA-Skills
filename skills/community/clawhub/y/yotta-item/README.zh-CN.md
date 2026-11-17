<p align="center"><b>语言</b>: 中文 · <a href="./README.md">English</a></p>

<p align="center">
  <img src="assets/banner.png" alt="yotta-item banner" width="100%" />
</p>

<h1 align="center">元题 yotta-item · 命题 / 组卷</h1>

<p align="center">YottaMeta 的<b>确定性组卷与试卷校验技能</b>：把双向细目表（题型、考点覆盖、难度配额、
分值、限时）与本地题库变成一份可复算的试卷——同一题库、蓝图与 seed 得到同一份选题；再用一次确定性检查
回答<b>「这份卷子总分、配比、覆盖、时间都达标吗」</b>。</p>
<p align="center">零依赖（Python 3.8+ 标准库），本地运行：不联网、不调用模型、不生成题面、不内置题目原文。</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue" /></a>
  <a href="https://agentskills.io/"><img alt="Standard: agentskills.io" src="https://img.shields.io/badge/standard-agentskills.io-orange" /></a>
  <a href="https://www.npmjs.com/package/@yottameta/yotta-item"><img alt="npm package" src="https://img.shields.io/npm/v/@yottameta/yotta-item" /></a>
</p>

## 这是什么

元题读取本地题库（题目 id、题型、分值、难度档、考点，可选预计作答时间与来源）与双向细目表（蓝图），产出两样东西：

- **组卷结果**：逐节选题——先保证必考考点覆盖，再按难度配额补足；同一题库、蓝图与 seed 得到同一份试卷；
- **试卷校验**：对已有试卷（只记题目 id 引用）列出确定性缺口——缺分节、题量与分值偏差、难度分布漂移、
  考点缺失、超出限时等。

它是命题辅助：不生成或改写题目内容与答案、不预测考后难度与区分度、不内置教材与真题原文。

## 核心价值

- **不编题**：每一道选中的题都来自题库；题目不够时报告缺口，不用编造的题顶替；
- **可复算**：固定 seed 的确定性选题，重跑与复核得到同一份试卷；
- **结论带证据**：每条缺口都给出题目 id、期望值与实际值；
- **本地零依赖**：Python 3.8+ 标准库，不联网、不调用模型、不上传题库与试卷；
- **实测边界诚实**：难度标注是题库相对口径；实测难度、区分度与掌握率属于考后的学情分析（元镜）。

## 快速开始

Windows 使用 `python`，Linux / macOS 使用 `python3`。

```bash
# 1. 生成模板（题库 + 蓝图 + 试卷）
python3 scripts/yotta_item.py template --output-dir ./item-template

# 2. 输入校验
python3 scripts/yotta_item.py bank validate --bank bank.json
python3 scripts/yotta_item.py blueprint validate --blueprint blueprint.json --bank bank.json

# 3. 按蓝图组卷（固定 seed，可复算）
python3 scripts/yotta_item.py assemble --bank bank.json --blueprint blueprint.json --seed 0

# 4. 校验试卷；有缺口即让 CI 失败
python3 scripts/yotta_item.py check --bank bank.json --paper paper.json \
  --blueprint blueprint.json --gate findings=1
```

## 命令一览

| 命令 | 说明 |
|---|---|
| `assemble --bank <文件> --blueprint <文件>` | 按蓝图从题库组卷 |
| `assemble --seed <n>` | 固定选题种子（默认 0） |
| `assemble --format md\|json` | Markdown（默认）或 JSON 输出 |
| `check --bank <文件> --paper <文件>` | 校验已有试卷（蓝图可选） |
| `check --blueprint <文件>` | 同时比对分节、分值、难度配额与覆盖 |
| `check --gate findings=<n>` | 缺口数量达到 `n` 时退出码 1 |
| `bank validate` / `blueprint validate` | CI 前置的输入校验 |
| `template --output-dir <目录>` | 生成题库 / 蓝图 / 试卷模板 |
| `--version` | 输出引擎版本 |

退出码：`0` 正常 ｜ `1` 触发闸门或组卷无法满足蓝图 ｜ `2` 输入错误 ｜
`3` 题库 / 蓝图 / 试卷校验错误 ｜ `4` 运行时错误。

## 题库

```json
{
  "schema_version": "1.0",
  "subject": "数学",
  "grade": "七年级上",
  "difficulty_levels": ["easy", "medium", "hard"],
  "items": [
    {
      "id": "SC-01",
      "type": "single_choice",
      "points": 3,
      "difficulty": "easy",
      "knowledge": ["一元一次方程的定义"],
      "minutes": 2,
      "source": "校本题库A"
    }
  ]
}
```

完整字段与错误表见 [references/bank-format.md](references/bank-format.md)。

## 双向细目表（蓝图）

```json
{
  "schema_version": "1.0",
  "title": "七年级上数学 第一单元测试",
  "total_points": 60,
  "time_limit_minutes": 60,
  "coverage": ["K3"],
  "sections": [
    {
      "id": "S1",
      "title": "选择题",
      "type": "single_choice",
      "count": 10,
      "points_each": 3,
      "difficulty": {"easy": 5, "medium": 3, "hard": 2},
      "knowledge": ["K1"]
    }
  ]
}
```

字段表、校验规则与写法建议见 [references/blueprint-format.md](references/blueprint-format.md)。

## 缺口类别

组卷：`insufficient_items` / `coverage_gap` / `time_over_budget`；
校验：`unknown_item` / `duplicate_item` / `total_points_mismatch` / `section_missing` /
`section_count_mismatch` / `section_type_mismatch` / `section_points_mismatch` /
`difficulty_mismatch` / `coverage_gap` / `time_over_budget` / `section_label_missing`。
定义、JSON 契约与退出码见 [references/report-format.md](references/report-format.md)。

## 边界

- 题目内容与答案来自题库，元题不生成、不改写；
- 难度标注是题库相对口径，不等于考后实测难度与区分度；
- 不做学生个体排名、评语与升学预测；
- 不内置教材、课标与真题原文；仓库内示例均为合成占位数据。

详见 [references/privacy.md](references/privacy.md)。

## 安装

### 方式一 · npx 一行装（推荐）

```bash
npx -y @yottameta/yotta-item --agent codex     # 也可 --agent claude | cursor | gemini | opencode ...
npx -y @yottameta/yotta-item --dir <技能目录>
```

### 方式二 · git clone

```bash
git clone https://github.com/YottaMeta/yotta-item.git <技能目录>/yotta-item
```

### 方式三 · 下载 ZIP

从 https://github.com/YottaMeta/yotta-item 下载 ZIP，解压到对应智能体的技能目录。

### 方式四 · install.sh

```bash
bash install.sh --list
bash install.sh --agent codex
bash install.sh --dir <技能目录>
```

## 配合使用

- **元案 yotta-lesson**：教案骨架的例题与练习位，按考点用元题选题；
- **元镜 yotta-mirror**：考后接手——实测难度、班级掌握率与学情诊断；
- **元呈 yotta-present**：把组卷与校验报告渲染成统一格式；
- **元忆 yotta-memory**：按需保存题库版本与组卷摘要（默认只在本机）。

## 环境要求

- Python 3.8+（仅标准库）
- UTF-8 编码的 JSON 题库 / 蓝图 / 试卷；无需额外依赖、数据库或服务

## 许可

MIT，见 [LICENSE](LICENSE) 与 [NOTICE](NOTICE)。
