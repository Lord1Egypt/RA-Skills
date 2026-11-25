# 使用细节

## 输入格式

推荐使用 UTF-8 Markdown 简历：

```markdown
# 姓名
手机号 | 邮箱

## 个人简介
2-3 句说明方向、经验和代表性成果。

## 工作经历
### 公司 | 岗位 | 开始时间 - 结束时间
- 我的动作 + 工具/流程 + 规模 + 结果。

## 技能
技能 A, 技能 B

## 教育背景
学校 | 专业 | 学历 | 开始时间 - 结束时间
```

DOCX 输入读取 WordprocessingML 正文；复杂文本框、页眉页脚和图片内文字可能丢失，
报告会给出解析提示。需要完整保留结构时建议使用可复制的 Markdown。

PDF 输入支持带文字层的本地 PDF，优先使用 PyMuPDF：

```bash
pip install pymupdf
python scripts/yotta_resume.py audit --resume resume.pdf --format json
```

报告会记录页数、图片数、文本字符数、SHA-256、解析后端和提示。加密、损坏或
扫描件不会生成伪完整报告。当前不执行 OCR；图片内信息会列入未知项。

旧版 `.doc`、网页或其它无法直接解析的内容，可先复制正文再传入：

```bash
python scripts/yotta_resume.py audit --resume-text - --format json < resume.txt
python scripts/yotta_resume.py interview start --resume-text - \
  --session session.json < resume.txt
```

## CLI

```bash
python scripts/yotta_resume.py --version
python scripts/yotta_resume.py quickstart --resume resume.md --jd jd.txt \
  --out-dir yotta-resume-action-pack
python scripts/yotta_resume.py selftest --quick
python scripts/yotta_resume.py selftest --full --json
python scripts/yotta_resume.py doctor --format json
python scripts/yotta_resume.py audit --resume resume.md --format markdown
python scripts/yotta_resume.py audit --resume-text - --format json < resume.txt
python scripts/yotta_resume.py audit --resume resume.md --jd jd.txt --format json
python scripts/yotta_resume.py interview start --resume resume.md --jd jd.txt --role-family soc --session session.json
python scripts/yotta_resume.py interview start --resume software.md --session software-session.json
python scripts/yotta_resume.py interview answer --session session.json --answer answer.md
python scripts/yotta_resume.py interview review --session session.json --format markdown
python scripts/yotta_resume.py export --input resume.md --docx resume.docx
python scripts/yotta_resume.py export --input resume.md --pdf resume.pdf
python scripts/yotta_resume.py contracts --format json
```

退出码：

- `0`：成功。
- `2`：命令参数不完整。
- `3`：输入文件不存在或无法读取。
- `4`：没有可用浏览器，或浏览器 PDF 渲染失败。
- `5`：PDF / DOCX 解析失败、扫描件不可提取、缺少 PDF 解析依赖或输入编码不支持。
- `6`：数据契约校验失败。

核心错误会在 stderr 返回稳定错误码、影响范围和下一步动作。例如
`YRS-INPUT-001` 表示输入文件不存在，`YRS-PDF-002` 表示 PDF 渲染失败，
`YRS-EXPORT-003` 表示行动包目录不可覆盖。

`interview start` 的 `--count` 范围为 `3-10`，默认 `6`。`--role-family`
无法唯一识别时必须显式传入；软件研发、数据与 AI、业务运营在行业信号明确时
自动映射对应岗位族，`generic` 只作受控回退；行业信号冲突时仍要求确认；
`--level` 缺省为 `mid` 并在会话中标记来源。
`interview answer --answer -` 从 stdin 读取。会话文件已存在时默认拒绝覆盖，
需要显式 `--force`。

`selftest --quick` 使用合成数据和临时目录检查核心执行路径；
`selftest --full` 增加表达边界、特殊输入和可选 PDF。`WARN` 表示可选依赖或
环境能力不可用，不阻断其他格式；`FAIL` 返回退出码 `6`。
`doctor` 仍可作为轻量环境检查。

`doctor` 的 `PASS` 表示核心能力可用，`WARN` 表示可选依赖缺失但不阻断其他格式，
`FAIL` 会导致退出码 `6`。默认 JSON 同时返回 `checks`、`warnings` 和 `errors`。

## 输出说明

- `audit` 的 JSON 使用 `schema_version: "1.1"`。
- `sections` 返回规范化章节名，如 `experience`、`projects`、`skills`、`education`。
- `industry_detection` 返回识别状态、主行业、置信度、命中关键词、候选行业、
  证据维度和岗位映射；信号接近时主行业为空并要求确认。
- `questions` 用于向求职者追问缺失事实；`suggestions` 只提供改写方向，不提供虚构数字。
- `jd_match` 包含 `matched`、`missing`、`coverage` 和 `status`；未提供 JD 时
  `coverage` 为 `null`。
- `jd_match.lexicon_version` 标识固定词表版本，`limitations` 说明它不做语义匹配、
  岗位排名或招聘竞争力判断。
- `readiness.score` 是“结构准备度（规则分）”，不代表招聘竞争力或招聘结果。
- `interview` 只输出证据状态、缺口和来源化学习重点，不输出面试分数、通过率
  或 Offer 预测；会话文件由用户显式指定，可删除。
- `clarity_review` 使用固定规则标记结果不可验证、责任边界不清和技能等级缺少证据，
  生成确认问题；不引入语义模型，也不生成新的主观分数。
- `quickstart --out-dir` 生成 `action-plan.md`、`audit-report.md` 和
  `action-pack.json`；目标目录必须不存在或为空。
- `issues` 中的每项 finding 包含稳定 ID、严重度、来源类型和待确认标记。
- `source_manifest`、`parse_warnings` 和 `unknowns` 用于说明输入质量与分析边界。
- 只能原样引用结构分；不得改写为其他数值、主观数字区间或“招聘方分数”。

## 数据契约

`contracts` 离线校验 7 个实际契约与 8 个 JSON Schema，包括行业注册表、
岗位族、证据账本、来源 registry、来源指纹状态、题库、双角色权限和面试会话状态。新增行业只需扩展
行业注册表与 Schema。详细字段见
[data-contracts.md](data-contracts.md)。

## PDF 要求

PDF 导出使用本机 Chromium、Chrome 或 Edge 的 headless 打印能力。没有浏览器时不会输出伪 PDF，请先安装任一受支持浏览器，或继续使用 DOCX/HTML。
每次尝试使用独立浏览器 profile；瞬态失败会自动重试，重试耗尽仍按事务化规则
清理半成品并保留原有同名文件。

## 多格式导出

DOCX / HTML / PDF 会先写入临时目录。所有请求格式成功后才提交到目标路径；
任一格式失败时不会留下本次部分成品，已有同名文件也会保留。多个输出参数指向
同一路径或目标路径是目录时，在写入前返回退出码 `2`。

## 数据边界

分析、模拟面试、`selftest`、`doctor`、`contracts` 和行动包生成不发起网络请求，
也不执行简历文本拼接出的 shell 命令。发布包不包含来源抓取能力。分析报告会遮蔽手机号、邮箱、URL、IP 和
客户名；正式导出的简历仍按原文保留联系方式，请只在需要投递时分享。
