<p align="center"><b>Language</b>: <a href="./README.md">English</a> · 中文</p>

<h1 align="center">yotta-resume · 元简</h1>

<p align="center">本地分析简历、追问缺失事实、给出修改建议，并导出 DOCX/PDF。</p>

<p align="center">
  <a href="LICENSE.txt"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue" /></a>
  <a href="https://www.npmjs.com/package/@yottameta/yotta-resume"><img alt="npm package" src="https://img.shields.io/npm/v/@yottameta/yotta-resume" /></a>
  <a href="https://github.com/YottaMeta/yotta-resume"><img alt="GitHub stars" src="https://img.shields.io/github/stars/YottaMeta/yotta-resume" /></a>
</p>

## 这是什么

元简是一个求职者简历分析与导出工具。它读取 Markdown、UTF-8 文本、DOCX
和文字层 PDF，根据简历可见内容自动识别行业，再识别章节、经历要点、量化指标、
联系方式和 JD 关键词缺口，输出高价值追问和修改建议；确认事实后，可以把同一份
简历导出为 DOCX、HTML 或 PDF。

核心分析使用 Python 标准库，不发起网络请求，不自动投递简历，也不编造经历或数字。
PDF 输入需要本地 PyMuPDF；未安装、扫描件或文件损坏时会明确降级或失败。

## 何时使用

- 需要诊断简历结构、经历证据或量化指标。
- 需要根据目标岗位 JD 判断关键词覆盖。
- 需要整理应向求职者追问的高价值问题。
- 需要运行由简历证据、JD 缺口和岗位题库驱动的单轮模拟面试与复盘。
- 需要把已确认的简历导出为 DOCX/PDF。

**不要使用**：代投简历、编造经历、预测面试或 Offer 结果、评估受保护个人属性，或制作复杂设计作品集排版。

## 快速使用

```bash
# 一次完成自检、分析、下一步提示和行动包
python scripts/yotta_resume.py quickstart --resume resume.md --jd jd.txt \
  --out-dir yotta-resume-action-pack

# 不读取用户简历，校验安装副本
python scripts/yotta_resume.py selftest --quick
python scripts/yotta_resume.py selftest --full --json

# 分析简历，输出 Markdown 报告
python scripts/yotta_resume.py audit --resume resume.md

# 直接分析文字层 PDF
python scripts/yotta_resume.py audit --resume resume.pdf

# 处理旧版文档或网页复制文本
python scripts/yotta_resume.py audit --resume-text - < resume.txt

# 结合 JD 分析，输出 JSON
python scripts/yotta_resume.py audit --resume resume.md --jd jd.txt --format json

# 开始本地单轮模拟面试
python scripts/yotta_resume.py interview start --resume resume.md --jd jd.txt \
  --role-family soc --level mid --session interview-session.json

# 非安全行业可省略岗位族，自动映射对应岗位族
python scripts/yotta_resume.py interview start --resume software.md \
  --session software-session.json

# 记录回答并查看证据缺口复盘
python scripts/yotta_resume.py interview answer --session interview-session.json --answer answer.md
python scripts/yotta_resume.py interview review --session interview-session.json

# 导出 DOCX、HTML 和 PDF
python scripts/yotta_resume.py export --input revised.md --docx revised.docx --html revised.html --pdf revised.pdf

# 离线校验岗位族、题库、来源与双角色权限契约
python scripts/yotta_resume.py contracts --format json
```

PDF 输出需要本机 Chromium、Chrome 或 Edge。没有浏览器时命令会返回明确错误，
不会生成伪 PDF；导出会使用独立浏览器 profile 并做有界重试。PDF 输入需要
`pip install pymupdf`。
多格式导出会先写入临时区，全部成功后再提交；PDF 失败不会留下本次 DOCX / HTML
半成品，也不会覆盖原有同名文件。

`interview` 会同时使用简历规则发现、JD 明确关键词缺口和版本化题库。
软件研发、数据与 AI、业务运营会映射到对应岗位族；`generic` 只作受控回退。
行业信号冲突时仍要求确认。
会话只写入显式传入的本地文件，可中断恢复，不联网、不调用模型、不写长期记忆。
回答只标记“证据充分 / 部分 / 缺失”，复盘不生成面试分数、通过概率或录用建议。

报告中的 `readiness.score` 只表示“结构准备度（规则分）”，不代表招聘方评分；
未提供 JD 时岗位覆盖为 `null`。JD 匹配使用版本化固定词表，会公开限制说明；
它不是语义匹配、岗位排名或招聘建议。不得把该分数改写成其他数值或主观数字区间。

行业识别使用版本化注册表。题库共 270 项：网络安全 6 个岗位族，加上软件研发、
数据与 AI、业务运营和通用岗位族，各 27 项；后续新增行业时
扩展 `data/industry-registry.json` 及 Schema 即可，不需要改主分析流程。

输入格式、字段和退出码见 [references/usage.md](references/usage.md)；
常见问题见 [references/faq.md](references/faq.md)；
数据契约见 [references/data-contracts.md](references/data-contracts.md)。

软件研发行业示例见 [examples/software-engineer.example.md](examples/software-engineer.example.md)；
HTML 成品样例见 [examples/export-samples](examples/export-samples/)；DOCX / PDF 请按导出命令在本地生成。

## 安装

以下四种方式任选；技能文件从 **npm** 获取，GitHub 供源码和 Issue 使用。

### 方式一：npm 一行装（推荐）

```text
npx -y @yottameta/yotta-resume@0.2.5 --agent <智能体名称>
npx -y @yottameta/yotta-resume@0.2.5 --dir <智能体的技能目录>
```

- `--agent <name>` 安装到该智能体默认用户级技能目录。
- `--dir <path>` 安装到指定技能目录。
- `--list` 查看已支持的智能体默认目录。
- 安装器只写入 `<目标>/yotta-resume`，仅在该目标内清理已知开发残留和缓存；安装根目录、目标及嵌套项中的任何符号链接或 junction 都会被拒绝。
- `--dry-run` 只显示目标，不写文件。核心简历流程在本地运行；只有用户主动执行锁版安装命令时才会访问软件包仓库。
- 国内镜像未同步新包时，可追加 `--registry=https://registry.npmjs.org/`。

### 方式二：git clone

```text
git clone https://github.com/YottaMeta/yotta-resume.git <智能体的技能目录>/yotta-resume
```

### 方式三：GitHub ZIP

在 `YottaMeta/yotta-resume` 仓库选择 **Code → Download ZIP**，解压后把 `yotta-resume` 放入智能体技能目录。

### 方式四：install.sh

```text
bash install.sh --agent <智能体名称>
bash install.sh --dir <技能目录>
bash install.sh --list
```

## 安装后校验

安装后运行 `python scripts/yotta_resume.py selftest --quick`。它使用合成数据检查
随包契约、分析、面试状态机、DOCX / HTML 导出、事务回滚和临时目录清理，不读取
用户简历。`selftest --full` 额外检查表达边界、特殊输入和可选 PDF；`doctor`
保留为轻量环境检查。

## 许可证

MIT © YottaMeta — 见 [LICENSE](./LICENSE.txt)。
