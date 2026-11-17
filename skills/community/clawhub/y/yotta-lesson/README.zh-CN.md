<p align="center"><b>语言</b>: 中文 · <a href="./README.md">English</a></p>

<p align="center">
  <img src="assets/banner.png" alt="yotta-lesson banner" width="100%" />
</p>

<h1 align="center">元案 yotta-lesson · 教案 / 学案</h1>

<p align="center">YottaMeta 的<b>确定性教案骨架与覆盖校验技能</b>：把课标映射包变成教案骨架——
环节时间精确到分钟、合计可校验，学习目标逐条带<b>课标来源</b>；再用一次确定性检查回答
<b>「知识点、环节、来源、时间都齐了吗」</b>。</p>
<p align="center">零依赖（Python 3.8+ 标准库），本地运行：不联网、不调用模型、不内置教材与题目原文。</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue" /></a>
  <a href="https://agentskills.io/"><img alt="Standard: agentskills.io" src="https://img.shields.io/badge/standard-agentskills.io-orange" /></a>
  <a href="https://www.npmjs.com/package/@yottameta/yotta-lesson"><img alt="npm package" src="https://img.shields.io/npm/v/@yottameta/yotta-lesson" /></a>
</p>

## 这是什么

元案读取课标映射包（课题 id、知识点、重难点、易错点、课标来源）与可选的结构配置，产出两样东西：

- **教案骨架**：学习目标（带来源）、重难点与易错点、五环节 + 分钟级时间分配、板书与评价清单；
- **覆盖检查**：对已有教案文本列出结构性缺口（未覆盖知识点、缺环节、缺来源、未标时间、合计时间不一致）。

它是备课辅助：不替教师写教学目标、不生成题目内容、不内置教材与题目原文。

## 核心价值

- **时间精确**：最大余数法分配，各环节分钟合计恒等于「课时 × 每课时分钟」；
- **来源可追**：每条学习目标都带映射包中的 `standard`；
- **确定性检查**：同一份教案、映射包与配置，得到同一份缺口清单；
- **本地零依赖**：Python 3.8+ 标准库，不联网、不调用模型、不上传教案；
- **只存结构性元数据**：映射包不含教材正文与题目原文。

## 快速开始

Windows 使用 `python`，Linux / macOS 使用 `python3`。

```bash
# 1. 生成模板（映射包 + 结构配置）
python3 scripts/yotta_lesson.py template --output-dir ./lesson-template

# 2. 生成教案骨架
python3 scripts/yotta_lesson.py plan --map lesson-map.json --lesson L1

# 3. 两课时版本，输出 JSON
python3 scripts/yotta_lesson.py plan --map lesson-map.json --lesson L1 --periods 2 --format json

# 4. 检查已有教案，缺口 ≥ 1 时让 CI 失败
python3 scripts/yotta_lesson.py check --plan plan.md --map lesson-map.json --lesson L1 --gate findings=1
```

## 命令一览

| 命令 | 说明 |
|---|---|
| `plan --map <文件> --lesson <id>` | 生成教案骨架 |
| `plan --periods <n>` | 覆盖映射包中的课时数 |
| `plan --format md\|json` | 输出格式：Markdown（默认）或 JSON |
| `check --plan <文件>` | 检查已有教案的结构性缺口 |
| `check --stdin` | 从标准输入读取教案文本 |
| `check --gate findings=<n>` | 缺口数量达到 n 时退出码 1 |
| `map list / show / validate` | 映射包列表 / 详情 / 校验 |
| `template --output-dir <目录>` | 生成映射包与结构配置模板 |
| `--version` | 打印引擎版本 |

退出码：`0` 正常 ｜ `1` 触发闸门 ｜ `2` 输入错误 ｜ `3` 映射或配置错误 ｜ `4` 运行时错误。

## 映射包示例

```json
{
  "schema_version": "1.0",
  "subject": "数学",
  "grade": "七年级上",
  "lessons": [
    {
      "id": "L1",
      "title": "认识一元一次方程",
      "periods": 1,
      "knowledge": ["一元一次方程的定义", "方程的解"],
      "misconceptions": ["把含未知数的式子都当方程"],
      "standard": "义务教育数学课程标准（2022 年版）· 方程与不等式"
    }
  ]
}
```

完整字段与报错对照见 [references/map-format.md](references/map-format.md)。

## 缺口类型

`knowledge_missing`、`stage_missing`、`source_missing`、`time_missing`、`minutes_mismatch`——
定义、报告契约与退出码见 [references/plan-format.md](references/plan-format.md)。

## 版权与边界

- 映射包只存结构性元数据，不内置教材、课标与题目原文；
- `standard` 是引用标注（用于可追溯），不代表本技能对课标作出解释；
- 输出为备课辅助，教学设计的最终决定由教师负责。

细节见 [references/copyright.md](references/copyright.md)。

## 安装

### 方式一 — npx 一行装（推荐）

```bash
npx -y @yottameta/yotta-lesson --agent codex     # 亦可 --agent claude | cursor | gemini | opencode ...
npx -y @yottameta/yotta-lesson --dir <技能目录>
```

### 方式二 — git clone

```bash
git clone https://github.com/YottaMeta/yotta-lesson.git <技能目录>/yotta-lesson
```

### 方式三 — 下载 ZIP

在 https://github.com/YottaMeta/yotta-lesson 页面点 Code → Download ZIP，解压到智能体的技能目录。

### 方式四 — install.sh

```bash
bash install.sh --list
bash install.sh --agent codex
bash install.sh --dir <技能目录>
```

## 与家族技能协同

- **元镜 yotta-mirror**：用学情数据反哺下一轮备课的薄弱点；
- **元题 yotta-item**：按双向细目表从学校自备题库组卷、并做试卷结构校验（不生成题面）；
- **元呈 yotta-present**：把教案骨架渲染成统一格式；
- **元真 yotta-humanize**：教师-facing 叙述文字去 AI 味；
- **元忆 yotta-memory**：按需保存映射包版本与骨架摘要。

## 运行要求

- Python 3.8+（仅标准库）
- UTF-8 的 JSON 映射包与教案文本；不需要额外依赖、数据库或服务

## 许可证

MIT，见 [LICENSE](LICENSE) 与 [NOTICE](NOTICE)。
