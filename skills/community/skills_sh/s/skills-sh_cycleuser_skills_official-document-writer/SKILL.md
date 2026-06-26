---
name: official-document-writer
version: "1.1.0"
description: |
  Official document writing assistant for Chinese government documents based on GB/T 9704-2012 standard.

  Triggers when: Writing Chinese official documents (公文), formatting documents according to national standards, reviewing document compliance, or creating notices, reports, requests, replies, letters, or minutes.

  Commands:
  - /gongwen notice <topic> - Write a notice (通知)
  - /gongwen report <topic> - Write a report (报告)
  - /gongwen request <topic> - Write a request (请示)
  - /gongwen reply <topic> - Write a reply (批复)
  - /gongwen letter <topic> - Write a letter (函)
  - /gongwen minutes <topic> - Write meeting minutes (纪要)
  - /gongwen check <document> - Check document compliance
  - /gongwen format - Show formatting rules

  Capabilities: 15 document types support, GB/T 9704-2012 compliance, hierarchy numbering rules, font and layout specifications, document structure templates
author: cycleuser
license: MIT
---

## Safety Rules

**Critical**: Read and follow [global-rules/bash-safety.md](file:///Users/fred/.config/opencode/skills/global-rules/rules/bash-safety.md) for all bash/command execution.

Core rules:
1. **Always set explicit `timeout` on bash calls** — 30s for tests, 60s for installs, never default
2. **Never run unscoped full test suites** — use `-k` or file paths to limit scope
3. **Never use `rm -rf` without variable guards**, `curl|bash`, `sudo`, or `kill -9`
4. **Infinite loops must have hard timeout + budget limits** — no unbounded while(True)
5. **Redirect stdin** with `< /dev/null` for non-interactive commands

A bash timeout that triggers SIGKILL corrupts the terminal FD, crashes opencode's TUI, and forces a GUI restart.

# Official Document Writer

Chinese official document writing assistant based on GB/T 9704-2012 national standard.

## Quick Commands

| Command | Description |
|---------|-------------|
| `/gongwen notice <topic>` | Write a notice (通知) |
| `/gongwen report <topic>` | Write a report (报告) |
| `/gongwen request <topic>` | Write a request (请示) |
| `/gongwen reply <topic>` | Write a reply (批复) |
| `/gongwen letter <topic>` | Write a letter (函) |
| `/gongwen minutes <topic>` | Write meeting minutes (纪要) |
| `/gongwen check <document>` | Check document compliance |
| `/gongwen format` | Show formatting rules |

## Document Types (公文种类)

According to "Regulations on the Handling of Official Documents of Party and Government Organs" (党政机关公文处理工作条例), there are 15 document types. Decision (决定) handles important matter deployment and rewards or punishments. Order (命令/令) publishes laws, appointments, removals, and commendations. Public Notice (公告) announces important matters domestically and internationally. Announcement (通告) publishes matters for general public knowledge. Notice (通知) handles approval and forwarding, deployment, and appointments. Circular (通报) praises excellence or criticizes mistakes. Proposal (议案) submits matters for deliberation. Report (报告) reports on work and responds to inquiries. Request (请示) requests instructions and approval. Reply (批复) responds to requests. Opinion (意见) provides insights and methods. Letter (函) handles work consultation and inquiry responses. Minutes (纪要) records main meeting circumstances.

## Document Structure (公文结构)

### Standard Format Elements

```
┌─────────────────────────────────────────────────────────────┐
│                        版头 (Header)                         │
├─────────────────────────────────────────────────────────────┤
│  份号 (保密件编号)                                           │
│  密级和保密期限 (如：机密★5年)                                │
│  紧急程度 (特急/加急)                                         │
│  发文机关标志 (红头)                                          │
│  发文字号 (如：国发〔2024〕1号)                               │
│  签发人 (上行文需标注)                                        │
├─────────────────────────────────────────────────────────────┤
│                        主体 (Body)                           │
├─────────────────────────────────────────────────────────────┤
│  标题 (居中，2号小标宋体)                                     │
│  主送机关 (顶格，3号仿宋)                                     │
│  正文 (3号仿宋)                                              │
│  附件说明                                                    │
│  发文机关署名                                                │
│  成文日期                                                    │
│  印章                                                        │
│  附注                                                        │
├─────────────────────────────────────────────────────────────┤
│                        版记 (Footer)                         │
├─────────────────────────────────────────────────────────────┤
│  抄送机关                                                    │
│  印发机关 / 印发日期                                         │
│  页码 (— 1 —)                                                │
└─────────────────────────────────────────────────────────────┘
```

### Letter Format Elements

```
┌─────────────────────────────────────────────────────────────┐
│                     信函格式 (Letter Format)                  │
├─────────────────────────────────────────────────────────────┤
│  发文机关名称 (居中)                                          │
│  发文字号 (右上角)                                            │
│  标题 (居中)                                                  │
│  主送机关                                                     │
│  正文                                                         │
│  发文机关署名                                                 │
│  成文日期                                                     │
│  印章                                                         │
└─────────────────────────────────────────────────────────────┘
```

## Formatting Rules (格式规范)

### Hierarchy Numbering (层次序号)

According to GB/T 9704-2012, the four-level hierarchy numbering system uses distinct formats at each level. The first level uses Chinese numerals with a pause (一、二、三、……). The second level uses full-width parentheses with Chinese numerals（（一）（二）（三）……). The third level uses Arabic numerals with an English period (1. 2. 3. ……)。 The fourth level uses full-width parentheses with Arabic numerals（（1）（2）（3）……). Note: Do NOT use Roman numerals (I, II, III) or other formats.

### Font Specifications (字体规格)

Different document elements require specific fonts and sizes. The发文机关标志 uses small standard Song typeface in red. The 标题 uses small standard Song typeface in size 2. The 主送机关 uses Fang Song in size 3. The first level of 正文 uses Hei in size 3. The second level of 正文 uses Kai in size 3. The third and fourth levels of 正文 use Fang Song in size 3. The 发文字号 uses Fang Song in size 3. The 页码 uses Song in size 4.

### Page Layout (页面设置)

Page layout follows strict specifications. Paper size is A4 (210mm × 297mm). Margins are top 37mm, bottom 35mm, left 28mm, right 26mm. Line spacing is fixed 28 pounds (approximately 0.99cm). Page number format is — 1 — (one dash + page number + one dash). Page number position is bottom center, odd pages on right, even pages on left.

### Date Format (日期格式)

The correct format is 2024年3月15日. Common errors include 二〇二四年三月十五日 (Chinese era format), 2024.03.15 (dot notation), and 2024-03-15 (dash notation). Use the Chinese character 年月日 format.

### Document Number Format (发文字号格式)

The correct format is 国发〔2024〕1号 using Chinese brackets. Common errors include 国发[2024]1号 with square brackets, 国发[2024]第1号 with the extra 第 character, and 国发（2024）1号 with parentheses instead of brackets. Use the Chinese bracket character 〔〕 without any additional characters.

## Workflow

```
Step 1: 确定公文类型
├── 分析发文目的
├── 确定行文关系
└── 选择公文文种

Step 2: 收集基本信息
├── 发文机关
├── 主送机关
├── 公文主题
└── 相关背景

Step 3: 撰写公文
├── 拟定标题
├── 撰写正文
├── 添加附件说明
└── 确定落款

Step 4: 格式检查
├── 层次序号
├── 字体字号
├── 页面设置
└── 整体排版

Step 5: 合规审核
├── 内容合法性
├── 格式规范性
├── 语言得体性
└── 程序完整性
```

## Rules

- [rules/document-types.md](rules/document-types.md) - Document types and usage
- [rules/formatting-rules.md](rules/formatting-rules.md) - GB/T 9704-2012 formatting rules
- [rules/writing-guidelines.md](rules/writing-guidelines.md) - Writing guidelines
- [rules/templates.md](rules/templates.md) - Document templates
- [rules/anti-aigc.md](rules/anti-aigc.md) - 公文写作反AIGC检测规则

## Writing Principles

Five principles guide official document writing. First, 准确 means content must be accurate and factual. Second, 简洁 means express ideas concisely. Third, 规范 means follow national standards strictly. Fourth, 得体 means use appropriate tone and language. Fifth, 完整 means include all necessary elements.

## Common Mistakes to Avoid

Six common mistakes compromise official document quality. Wrong hierarchy numbering format violates the standard numbering rules. Missing document number or date makes the document incomplete. Incorrect font or size fails to meet formatting specifications. Missing stamp or signature invalidates the document. Wrong tone for document type inappropriate for the specific公文种类. Incomplete document structure violates the required format.

## Reference Standards

- GB/T 9704-2012 党政机关公文格式
- 党政机关公文处理工作条例 (2012)
- 标点符号用法 (GB/T 15834-2011)

## 示例 (Examples)

### 通知示例
```
XX市人民政府办公室关于做好2026年防汛工作的通知

各区县人民政府，市各委办局：

为切实做好2026年防汛工作，保障人民群众生命财产安全，现将有关事项通知如下：

一、加强组织领导。各区县要成立防汛指挥部...
二、排查风险隐患。对辖区内河道、水库、地质灾害点...
三、做好应急准备。储备防汛物资，组建应急队伍...

XX市人民政府办公室
2026年5月9日
```

### 报告示例
```
关于XX项目进展情况的报告

XX领导：

根据工作安排，现将XX项目进展情况报告如下：

一、工作进展。已完成...达到预期进度的80%...
二、存在问题。资金到位率仅60%，影响土建工程进度...
三、下一步计划。加快资金筹措，预计6月底完成主体工程...

特此报告。

XX单位
2026年5月9日
```

## 边界情况 (Edge Cases)

- **联合发文**: 多个单位联合发文时，主办单位排在前面，使用主办单位的发文字号
- **紧急公文**: 标注"特急"或"加急"，处理时限分别为3天和5天
- **涉密文件**: 在版头右上方标注密级和保密期限，不得以电子形式传输
- **附件处理**: 在正文下空一行标注"附件："及名称；多个附件用阿拉伯数字编号
- **抄送机关**: 除主送机关外需执行或知晓的机关，用4号仿宋体左空一字编排
- **印发传达范围**: 在附注位置标注，如"(此件公开发布)"或"(发至县团级)"

## 常见问题与排查

- **发文字号错误**: 检查发文机关代字、年份(六角括号〔〕)、序号是否正确
- **标题要素缺失**: 标题必须包含发文机关、事由、文种三要素
- **主送机关遗漏**: 确保所有需要执行或知悉的机关都列在主送栏
- **附件标注遗漏**: 正文中提及的附件必须在附件说明中标注

## AIGC-Aware Output

Official documents (公文) must be GB/T 9704-2012 compliant AND avoid template-filling AI patterns. Good 公文 reads like "领导的意思很明确"; AI 公文 reads like "this paragraph could go in any notice". See `rules/anti-aigc.md` for complete detection rules.

Key requirements:
- Every deployment must have deadline, responsible person, and specific quantities
- Replace "进一步加强" with concrete action + timeline: "6月底前完成527处隐患排查"
- Replace "切实做好" with specific measure: "4月15日前完成3支应急队伍组建"
- Break paragraph-opening symmetry: not every paragraph starts with "加强/强化/做好/严格"
- Eliminate "进一步/持续/深入/切实" when frequency exceeds 3 per 1000 characters

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-04-01 | 初始版本，GB/T 9704-2012标准支持 |
| 1.1.0 | 2026-05-09 | 添加安全规则、示例、边界情况、排查指南 |

## See Also / 相关技能

- `/人话` from **humanizer** — 在适当场景下，将公文语言人化处理 / Humanize official document language when appropriate