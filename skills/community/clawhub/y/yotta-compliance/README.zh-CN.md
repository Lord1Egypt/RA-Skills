<p align="center"><b>Language</b>: <a href="./README.md">English</a> · 中文</p>

<p align="center">
  <img src="assets/banner.png" alt="yotta-compliance banner" width="100%" />
</p>

<h1 align="center">yotta-compliance · 元规 (YuanGui)</h1>

<p align="center">YottaMeta 的 <b>确定性合规条款审查技能</b>：用版本化 JSON 规则包审查 UTF-8 文本或
Markdown，每条 finding 都回到 <b>原文证据、命中规则、框架覆盖级别与来源条款</b>。</p>
<p align="center">当前 <b>baseline_review</b> 规则包：PIPL（11 条）与数据出境（4 条）。
GDPR / HIPAA / SOC2 / PCI-DSS / ISO27001 / 等保 为 <b>mapping_only</b> 主题标签，
不输出这些框架的独立合规结论。</p>
<p align="center">纯 Python 3.8+ 标准库，零外部依赖；Windows + Linux + macOS；
审查路径纯本地运行，不联网、不调用模型。</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue" /></a>
  <a href="https://agentskills.io/"><img alt="Standard: agentskills.io" src="https://img.shields.io/badge/standard-agentskills.io-orange" /></a>
  <a href="https://www.npmjs.com/package/@yottameta/yotta-compliance"><img alt="npm package" src="https://img.shields.io/npm/v/@yottameta/yotta-compliance" /></a>
  <a href="https://github.com/YottaMeta/yotta-compliance"><img alt="GitHub stars" src="https://img.shields.io/github/stars/YottaMeta/yotta-compliance" /></a>
  <a href="https://github.com/YottaMeta/yotta-compliance/commits/main"><img alt="last commit" src="https://img.shields.io/github/last-commit/YottaMeta/yotta-compliance" /></a>
</p>

## 这是什么

元规用确定性规则审查文本或 Markdown 条款：解析文档结构、匹配规则候选、求值断言、抽取原文证据、
计算框架覆盖标签，最后输出人类可读的 Markdown 报告与稳定的 JSON 契约。

它是审查辅助工具，不是法律意见。每条风险结论必须对应原文证据、规则 id 与来源条款；
规则找不到证据时，不会凭空生成风险结论。

## 核心价值

- **证据优先**——每条 `matched_span` 的 quote 都来自原文切片，带原始 `start` / `end` 偏移与行列号。
- **确定性**——同一输入、同一规则包、同一参数得到同一结果，重复运行只有 `generated_at` 变化。
- **规则包版本化**——报告记录 `pack_id`、`pack_version`、覆盖级别与 SHA-256。
- **覆盖级别显式**——`baseline_review` 可输出独立 finding；`mapping_only` 只是主题标签，
  不得解读为已完成该框架审查。
- **稳定 JSON 契约**——固定顶层字段，便于自动化、审计留痕与 CI 闸门。
- **本地零依赖**——Python 3.8+ 标准库；无网络、无模型、无数据库。

## 覆盖范围

| 规则包 | 框架 | 覆盖级别 | 规则数 |
|---|---|---|---|
| `pipl` | PIPL | `baseline_review` | 11 |
| `data-export` | 数据出境 | `baseline_review` | 4 |

GDPR / HIPAA / SOC2 / PCI-DSS / ISO27001 / 等保 为 `mapping_only`：只接收主题标签，
报告不输出这些框架的独立结论。

完整规则清单、来源条款、主题映射与明确未覆盖范围见
[references/coverage.md](references/coverage.md)。

## 命令一览

| 命令 | 说明 |
|---|---|
| `review --input <file>` | 审查 UTF-8 `.txt` / `.md` / `.markdown` 文件 |
| `review --stdin` | 从标准输入读取文本 |
| `review --frameworks <list>` | 按逗号分隔的规则包 id 选择；缺省装载全部规则包 |
| `review --format md\|json` | 输出 Markdown（默认）或 JSON |
| `review --out <file>` | 写报告文件；缺省写 stdout |
| `review --gate <level>` | CI 闸门：`off` / `low` / `medium` / `high` / `critical` |
| `review --min-severity <level>` | 只输出达到该严重度的 finding |
| `review --include-safe` | 列出已检查但未命中的规则 |
| `rules list` | 列出规则包与规则 |
| `rules show <rule_id>` | 查看单条规则的说明、建议、来源与测试用例 |
| `rules validate --pack <file>` | 校验规则包；结构错误立即失败 |

退出码：**0** 审查完成且未触发 gate；**1** 触发 gate；**2** 输入 / 编码 / 路径错误；
**3** 规则包错误；**4** CLI 用法错误。

## 快速使用

Windows 使用 `python`，Linux / macOS 使用 `python3`。

```bash
# 使用默认规则包审查
python3 scripts/yotta_compliance.py review --input contract.md

# 只使用 PIPL 规则包
python3 scripts/yotta_compliance.py review --input contract.md --frameworks pipl

# JSON 报告 + high 级 CI 闸门
python3 scripts/yotta_compliance.py review --input contract.md --format json --gate high --out report.json

# 从标准输入读取
python3 scripts/yotta_compliance.py review --stdin --frameworks pipl,data-export

# 查看与校验规则包
python3 scripts/yotta_compliance.py rules list --framework pipl
python3 scripts/yotta_compliance.py rules show PIPL-NOTICE-001
python3 scripts/yotta_compliance.py rules validate --pack rules/pipl.json
```

报告默认写 stdout；只有显式提供 `--out` 才写文件。输出路径不得覆盖输入文件，也不得写入规则包目录。

## 示例

输入片段：

```text
我们收集你的个人信息，用于提供服务。
保存期限：3年。
数据出境至境外服务器。
```

对一份缺少多项护栏的说明运行默认规则包，汇总示例：

```text
- 本次输出 11 条发现（全部 11 条）
- high：3 条
- medium：4 条
- low：4 条
- 已检查规则：15 条 ｜ 命中规则：13 条
```

实际结果取决于输入内容与所选规则包；示例数字不是固定输出。`--gate high` 在上述结果下返回退出码 1。

## 报告契约

Markdown 报告固定包含七节：输入摘要、框架覆盖摘要、风险汇总、逐条发现、未覆盖范围、
人工复核清单、免责声明。

JSON 报告固定提供：

```json
{
  "schema_version": "1.0",
  "tool": "yotta-compliance",
  "tool_version": "0.1.0",
  "generated_at": "2026-09-24T12:00:00Z",
  "input": {},
  "rule_packs": [],
  "framework_coverage": [],
  "summary": {},
  "findings": [],
  "review_items": [],
  "disclaimer": "本工具提供基于确定性规则的条款审查建议与证据链，不构成法律意见。"
}
```

字段语义、证据结构与过滤行为见 [references/report-format.md](references/report-format.md)。

## 已知局限

- **词形匹配，不是语义理解**——absence 规则只判断检索词是否出现；同义但词形不同的表述可能漏检。
- **文档级 absence 范围**——检索词出现在文档任何位置都视为已出现，不判断其是否适用于当前处理活动。
- **否定句不建模**——“不会对外提供”等否定表述仍可能触发候选匹配。
- **只解析阿拉伯数字**——`保存期限：N年` 可解析；“三年”等中文数字不做解析或换算。
- **数据出境人数阈值未进入 v1**——需要单位感知的数值原语；为避免输出可能错误的数值结论，
  相关阈值规则推迟到规则包 v2。
- **absence 结论降低置信度**——medium / low 置信 finding 进入人工复核清单，必须人工核验后才能采信。
- **不直接解析 PDF / docx**——需先转成 UTF-8 文本或 Markdown。
- **`mapping_only` 不是审查**——它只是主题标签。

## 数据与安全边界

- 纯本地运行；不上传原文、证据或报告，不联网检索法条；
- 规则包是只读数据，规则正文不会被执行；
- 输入上限 2 MiB，仅接受 UTF-8 文本；
- 除非显式设置 `--out`，报告只写 stdout；
- 输出路径防护禁止覆盖输入文件与写入规则包目录；
- 不缓存原文，不把合同内容写入日志。

## 在智能体中使用

1. 按下方「安装」把技能装入智能体的技能目录；
2. 用户要求审查 PIPL 或数据出境条款时，对提供的文本 / Markdown 运行 `review`；
3. 先说明覆盖摘要：哪些框架是 `baseline_review`，哪些只是 `mapping_only`；
4. 按严重度逐条说明 finding，引用原文证据与规则来源条款；
5. 低置信 finding 一律作为人工复核项处理，不当作最终法律结论；
6. 除非用户明确要求另存报告，不修改原文档。

## 安装

以下四种方式任选，顺序即推荐优先级；技能文件一律从 **npm** 获取（GitHub 无代理较慢，
npm 支持镜像）。

### 方式一：npm 一行装（推荐）

```text
# 可选国内加速：npm config set registry https://registry.npmmirror.com
npx -y @yottameta/yotta-compliance --agent <智能体名称>      # 装到指定智能体默认用户级技能目录
npx -y @yottameta/yotta-compliance --dir <智能体的技能目录>  # 指到技能目录本身
```

- `--agent <name>` 自动装到该智能体默认用户级目录；`--list` 可查看各智能体默认目录。
- `--dir <路径>` 装到指定技能目录；未收录的智能体用 `--dir` 指到它的技能目录。
- npmmirror 未同步新包（404）：加 `--registry=https://registry.npmjs.org/`（国内需代理），
  或稍等镜像缓存。

### 方式二：git clone（开发者 / 有 git 环境）

```text
git clone https://github.com/YottaMeta/yotta-compliance.git <智能体的技能目录>/yotta-compliance
```

### 方式三：GitHub 下载压缩包（手动 / 无 git 环境）

在 GitHub 仓库 `YottaMeta/yotta-compliance` 点 **Code → Download ZIP**，解压后把
`yotta-compliance` 文件夹放进智能体技能目录。

### 方式四：install.sh（多智能体一键脚本）

```text
bash install.sh --agent <name>   # 装到指定智能体默认用户级目录
bash install.sh --dir <path>     # 装到指定目录
bash install.sh --list           # 列出智能体 -> 默认目录
```

> 方式一走 npm 源（npmmirror / npmjs），不依赖 GitHub；方式二 / 三走 GitHub，国内无代理可能失败。

## 开发与校验

```bash
# 契约测试（技能目录内运行）
python3 scripts/test_yotta_compliance.py

# 规则包校验
python3 scripts/yotta_compliance.py rules validate --pack rules/pipl.json
python3 scripts/yotta_compliance.py rules validate --pack rules/data-export.json

# 语法检查
python3 -m py_compile scripts/yotta_compliance.py
```

规则编写规范见 [references/rule-authoring.md](references/rule-authoring.md)。

## 边界与免责声明

元规提供基于确定性规则的条款审查建议与证据链，不构成法律意见，不替代律师或合规顾问，
也不判断合同效力、监管审批或诉讼结果。规则命中只描述文本中出现的可观察现象，不代表真实业务
一定未履行义务；规则未命中也不代表不存在风险。`mapping_only` 框架不得被描述为已审查或已认证。
请只审查有权处理的内容，最终判断由具备资质的专业人士作出。

## 许可证

[MIT](./LICENSE) © YottaMeta。YottaMeta 家族名称与 `yotta-*` 前缀是 YottaMeta 品牌标识；
衍生作品不得复用，详见 [NOTICE](./NOTICE)。
