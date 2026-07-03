# 精神病学 Psychiatry-PMPH-9edition

<div align="center">

> *「21世纪医学生指南」*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Skills](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)

<br>

> 基于人民卫生出版社《精神病学》第9版的临床技能手册 — **47 项精神科核心临床技能**

<br>

何必苦苦读一本书<br>
只需输入一个问题，自动从课本中找到解决方案

<br>

**其他语言 / Other Languages:**

[English](README_EN.md) · [日本語](README_JP.md) · [Français](README_FR.md) · [Русский](README_RU.md)

</div>

---

## 项目简介

本项目系统整合精神病学、临床心理学及精神康复领域的全面知识与实践指南，涵盖 **47 项关键临床技能**，分为 8 大分类：基础评估与诊断研究、心境焦虑与强迫障碍、精神分裂症与精神病性障碍、神经认知与老年精神障碍、躯体进食睡眠与物质使用障碍、人格发育创伤与分离障碍、急诊危机干预与司法伦理、康复社区与综合管理。

**适用人群**：精神科医师、心理治疗师、医学生、社区精神卫生工作者、综合医院会诊联络团队

**参考教材**：人民卫生出版社《精神病学》第 9 版

**⚠️ 风险警示 ⚠️**：该技能涵盖精神科诊断、药物治疗、危机干预、司法鉴定及康复管理等主题，这些内容可能被误用为独立的医疗建议。

**缓解措施**：仅将输出作为教育或临床医生审核的参考资料使用，并根据当前官方指南、本地方案和合格精神科专家核实建议。

**⚠️ 风险警示 ⚠️**：源内容并不始终严格执行仅限临床医生的安全界限。

**缓解措施**：部署系统级医疗安全政策，要求升级至合格精神科医生进行诊断、开具处方、剂量分配、急诊护理及自我治疗决策。

## 项目结构

```
psychiatry-pmph-9edition/
├── SKILL.md                    # 核心配置 — 47 项技能注册表
├── README.md                   # 本文档 — 项目说明与使用指南
├── README_EN.md                # 英文版说明
├── README_JP.md                # 日文版说明
├── README_FR.md                # 法文版说明
├── README_RU.md                # 俄文版说明
├── <skill-name>/               # 各子技能目录
│   ├── SKILL.md                #   技能详情（使用时机、执行步骤、注意事项、参考文档）
│   └── references/             #   详细参考资料（可选）
│       └── *.md
├── .clawhubignore              # ClawHub发布忽略规则
└── .gitignore                  # Git忽略规则
```

## 技能分类一览

### 基础评估与诊断研究

| 技能数 | 说明 |
|--------|------|
| 4 | 临床评估、诊断推理、分类编码、RDoC研究框架 |

### 心境、焦虑与强迫相关障碍

| 技能数 | 说明 |
|--------|------|
| 5 | 抑郁障碍、双相障碍、焦虑障碍、OCD及相关障碍 |

### 精神分裂症与精神病性障碍

| 技能数 | 说明 |
|--------|------|
| 3 | 精神分裂症谱系、重性精神障碍管理、思维障碍评估 |

### 神经认知与老年精神障碍

| 技能数 | 说明 |
|--------|------|
| 6 | AD、痴呆筛查、DLB、谵妄、神经认知评估、会诊联络 |

### 躯体、进食、睡眠与物质使用障碍

| 技能数 | 说明 |
|--------|------|
| 11 | 进食障碍、ARFID、躯体痛苦障碍、睡眠障碍、物质使用、笑气滥用 |

### 人格、发育、创伤与分离障碍

| 技能数 | 说明 |
|--------|------|
| 6 | 人格障碍、神经发育障碍、抽动障碍、PTSD、分离障碍、围产期管理 |

### 急诊、危机干预与司法伦理

| 技能数 | 说明 |
|--------|------|
| 5 | 危机干预、非自愿治疗、司法鉴定、伦理合规 |

### 康复、社区与综合管理

| 技能数 | 说明 |
|--------|------|
| 7 | 社区康复、ISP、住院康复、预防体系、药物治疗管理 |

> 完整 47 项技能详情请参见 [SKILL.md](SKILL.md)

## 快速开始

### 安装

CLI：
```bash
openclaw skills install psychiatry-pmph-9edition
```

Prompt：
```bash
Before installing anything, inspect the ClawHub skill metadata and setup requirements.
If the skill asks you to install a third-party package or CLI, verify its source, maintainer, and package contents before running the install command.
Install the skill "Psychiatry-PMPH-9edition" from ClawHub only after those checks pass.
Skill page: https://clawhub.ai/psychiatry-pmph-9edition
Keep the work scoped to this skill only.
After install, help me finish setup from verified skill metadata.
Use only the metadata you can verify from ClawHub; do not invent missing requirements.
Ask before making any broader environment changes.
```

### 使用方式

每个子技能包含四部分内容：
1. **使用时机** — 何时触发该技能
2. **工作流程** — 标准化操作流程
3. **关键决策点** — 重要注意事项与约束
4. **参考文档** — 详细补充资料

### 提问策略

#### 1. 概念查询
**Question:**
```bash
精神分裂症的阳性症状与阴性症状
```
**Answer:**
参见 `schizophrenia-spectrum-disorders` 技能，输出结构化的诊断标准与症状分类。

#### 2. 临床案例分析
**Question:**
```bash
一名 45 岁女性，表现为情绪低落、早醒、食欲减退 2 个月，近期出现自杀意念，应如何评估和处理？
```
**Answer:**
综合调用 `depressive-disorders-comprehensive-management` 与 `psychiatric-emergency-crisis-intervention` 技能，完成诊断分型、自杀风险评估与综合治疗方案制定。

#### 3. 治疗决策
**Question:**
```bash
双相障碍急性躁狂发作的药物治疗选择
```
**Answer:**
调用 `mood-disorders` 或 `bipolar-schizophrenia-management` 技能，输出药物推荐、剂量滴定方案及不良反应监测要点。

### 快速导航

- "请制定一名自杀风险中度的抑郁障碍患者的危机干预计划。"
- "依据「精神分裂症谱系障碍」技能，分析一名偏执型精神分裂症患者的诊断与用药调整。"
- "参考「社区康复 ISP 管理」技能，为一名慢性精神分裂症患者制定个别化服务计划。"

## 关于作者

**改编自 OpenClaw 社区** — 基于人民卫生出版社《精神病学》第 9 版整理

## 技术支持

- PDF2App 项目：https://pdf2app.cn
- Microsoft Visual Studio Code：https://code.visualstudio.com/
- Claude Code for VS Code：https://claude.com/
- DeepSeek API：https://platform.deepseek.com/
- Xiaomi Mimo API：https://platform.xiaomimimo.com/

## 许可证

本项目内容基于人民卫生出版社《精神病学》第9版整理，仅供学习参考。发布遵循 MIT-0 许可证。
