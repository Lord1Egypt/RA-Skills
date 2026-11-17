<p align="center"><b>语言</b>: 中文 · <a href="./README.md">English</a></p>

<p align="center">
  <img src="assets/banner.png" alt="yotta-school-doc banner" width="100%" />
</p>

<h1 align="center">元公 yotta-school-doc · 学校公文校验</h1>

<p align="center">YottaMeta 的<b>学校公文可信起草与校验技能</b>：把版本化文种规则包与结构化事实变成
可复算的文书骨架，再对已有文稿检查必填字段、结构段、日期格式与先后关系、事实日期一致性、附件、
未定占位值、学生个人信息、过度承诺、敏感表述和会议待办完整性。</p>
<p align="center">零依赖（Python 3.8+ 标准库），本地运行：不联网、不调用模型、不上传、不编造事实。</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue" /></a>
  <a href="https://agentskills.io/"><img alt="Standard: agentskills.io" src="https://img.shields.io/badge/standard-agentskills.io-orange" /></a>
  <a href="https://www.npmjs.com/package/@yottameta/yotta-school-doc"><img alt="npm package" src="https://img.shields.io/npm/v/@yottameta/yotta-school-doc" /></a>
</p>

## 为什么做

学校公文重复、繁琐，而且风险不低：日期写错、附件漏传、`〔待补〕` 没删、学生个人信息混入公开文书，
都可能带来实际麻烦。通用写作工具擅长把文字写顺；元公只做一个更小、更可验证的事：

- 把缺失事实统一显示为 `〔待补〕`；
- 把结构缺口变成可复算、可复核的清单；
- 让文稿与校情数据留在本机。

## 功能

- 内置 8 个文种：通知、告家长书、请示、报告、工作总结、会议纪要、工作方案、简报；
- `draft`：按事实 JSON 生成 Markdown / JSON 文书骨架；
- `check`：对已有文稿做确定性检查，结论带证据行；
- `types`：查看、展示、校验内置或自定义规则包；
- `--gate findings=n`：缺口数量达到阈值时让 CI 失败；
- 零依赖 Python 3.8+ 标准库；不联网、不调用模型。

## 快速开始

```bash
python3 scripts/yotta_school_doc.py template --output-dir ./school-doc-template
python3 scripts/yotta_school_doc.py draft --type notice --facts facts.json
python3 scripts/yotta_school_doc.py check --doc notice.md --type notice --facts facts.json --gate findings=1
python3 scripts/yotta_school_doc.py types list
```

退出码：`0` 正常，`1` 触发闸门，`2` 输入错误，`3` 文种或规则包错误，`4` 运行时错误。

## 输入

事实清单是 JSON 对象：

```json
{
  "schema_version": "1.0",
  "doc_type": "notice",
  "visibility": "public",
  "title": "关于开展秋季运动会的通知",
  "issuer": "示例中学",
  "published_date": "2026-09-24",
  "audience": "各年级组、各班级",
  "action_deadline": "2026-09-30",
  "contact": "教务处（010-00000000）",
  "body_points": ["运动会时间与地点", "报名办法", "安全工作要求"],
  "attachments": ["报名表.xlsx"]
}
```

日期支持 `YYYY-MM-DD` 与 `YYYY年M月D日`，内部会归一化后再比较。缺失事实会写成 `〔待补〕` 并进入缺口清单。

## 检查项

`check` 会输出确定性缺口，例如 `field_missing`、`section_missing`、`date_format_invalid`、
`date_order_invalid`、`fact_date_mismatch`、`attachment_missing`、`attachment_unknown`、
`placeholder_present`、`privacy_risk`、`action_item_incomplete`、`sensitive_term_review`、
`overclaim_review`。

每条缺口包含严重级、处理建议与证据对象；能定位到原文时给出行号和引用。

## 隐私与边界

- 不联网、不调用模型；
- 学校文稿与校情数据只在本机流转；
- 个人信息检查只做规则命中提示，不做身份判断；
- 不内置标准全文、真实学校模板或案例正文；
- 输出是文书辅助与风险提示，不构成法律、合规、督导或意识形态审查结论；最终签发责任在学校。

## 安装

### 方式一 npx 一行装（推荐）

```bash
npx -y @yottameta/yotta-school-doc --agent <智能体名称>
npx -y @yottameta/yotta-school-doc --dir <智能体技能目录>
```

### 方式二 git clone

```bash
git clone https://github.com/YottaMeta/yotta-school-doc.git <智能体技能目录>/yotta-school-doc
```

### 方式三 Download ZIP

在 GitHub 仓库页面点击 Code → Download ZIP，解压到智能体技能目录。

### 方式四 install.sh

```bash
bash install.sh --list
bash install.sh --agent <智能体名称>
bash install.sh --dir <智能体技能目录>
```

## 开发

```bash
python3 scripts/test_yotta_school_doc.py
```

引擎是单文件、标准库实现：`scripts/yotta_school_doc.py`。

## 许可

MIT
