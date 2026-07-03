# 🏛️ 智慧招采通 Smart Procurement Navigator v2.0.0

[![Version](https://img.shields.io/badge/version-2.0.0-blue)](https://github.com/yinjianheng/smart-procurement-navigator)
[![License](https://img.shields.io/badge/license-Personal%20Use%20Only-red)](./LICENSE)
[![Author](https://img.shields.io/badge/author-yinjianheng-orange)](https://github.com/yinjianheng)
[![Platform](https://img.shields.io/badge/platform-WuKong%20%7C%20Claude%20%7C%20OpenClaw-brightgreen)](https://github.com/yinjianheng)

> **AI 招投标全流程智能助手 | 商机甄别 → 投标研判 → 标书编制 → 合规审查 | 12 大环节一站式闭环**
>
> 深度适配《中华人民共和国招标投标法》《中华人民共和国政府采购法》框架，覆盖政府采购、工程建设、服务类项目全场景。

---

## 🎯 为什么选择智慧招采通？

| 痛点 | 智慧招采通的解决方案 |
|------|---------------------|
| 📄 采购文件几百页，关键信息难提取 | **智能解读**：自动提炼资格门槛、评审办法、否决条款 |
| 📊 评分标准复杂，不知道如何分配精力 | **评审模型构建**：区分否决项/评分项，输出应答章节映射 |
| ✍️ 标书编写耗时数周，质量参差不齐 | **AI 辅助写作**：根据评审要项产出章节初稿，消除模板化表达 |
| ⚠️ 废标风险高，一次疏忽满盘皆输 | **合规审查**：30+ 常见废标原因自动检测，呈交前终审放行 |
| 📅 时间节点多，容易错过关键截止 | **时间预警**：20+ 关键时间节点自动提醒 |

---

## 🚀 核心能力矩阵

| 序号 | 环节 | 能力 | 输出 |
|------|------|------|------|
| 1 | 🎯 商机甄别 | 采购公告智能解析 | 商机摘要 + 时间节点预警 |
| 2 | 📋 投标研判 | 资质/业绩/预算/竞争四维评估 | 投标可行性报告 |
| 3 | 🔍 文件解读 | 资格门槛/评审办法/否决条款提取 | 结构化解读报告 |
| 4 | 🗂️ 资料结构化 | 采购文件→可检索文本 | 结构化知识库 |
| 5 | 📊 评审建模 | 否决项 vs 评分项 vs 客观分 | 评审计分模型 + 应答映射 |
| 6 | 📝 任务分解 | 资料清单 + 责任人 + 截止时间 | 应标任务清单 |
| 7 | 🏗️ 架构设计 | 前置索引 + 章节目录 + 篇幅规划 | 应答方案架构 |
| 8 | ✍️ 文稿生成 | 按评审项 + 技术规范产出 | 章节初稿 |
| 9 | 🎨 润色增强 | 去模板化 + 图表占位索引 | 润色后文稿 |
| 10 | ✅ 合规审查 | 缺项/格式/偏离/否决风险 | 合规审查报告 |
| 11 | 🔒 呈交终审 | 一致性校验 + 签章核查 | 终审放行单 |
| 12 | 📚 经验沉淀 | 中标/未中标根因分析 | 可复用素材库 |

---

## 📦 快速开始

```bash
# 安装到 WuKong / Claude / OpenClaw
cp -r smart-procurement-navigator ~/.claude/skills/

# 触发方式：直接描述需求
"帮我分析这份政府采购公告"
"这份招标文件的资格门槛是什么？"
"按评审标准生成应答方案架构"
"做一次标书合规审查"
```

---

## 🏆 特色亮点

- **法律合规深度**：内置《招标投标法》《政府采购法》及实施条例、2024 国办发 21 号文、2025 远程异地评标新规
- **评标方法全覆盖**：综合评分法（固定分值/区间赋分/排序赋分）+ 价格分异常识别
- **电子招投标适配**：远程异地评标主场/副场机制、电子签章 CA 互认
- **废标规避**：30+ 常见废标原因及规避策略
- **救济机制**：质疑→投诉→复议三级（7→15→60 日时限）
- **中小企业优惠**：联合体投标、资格预审 vs 资格后审、双信封制

---

## 📁 文件结构

```
smart-procurement-navigator/
├── SKILL.md                    # 核心技能文件（777 行）
├── README.md                   # 本文件
├── agent.yaml / system_prompt.md / workflows.md / runbook.md
├── skills/procurement_skills.yaml
├── knowledge/README.md
├── templates/                  # 7 个专业模板
│   ├── opportunity_brief.md    # 商机摘要
│   ├── tender_analysis_report.md # 招标分析报告
│   ├── score_model.md          # 评审模型
│   ├── response_outline.md     # 应答大纲
│   ├── service_scheme_structure.md # 服务方案结构
│   ├── review_report.md        # 审查报告
│   └── consistency_check_report.md # 一致性检查
├── test_cases/p0_demo_cases.md
└── demo/demo_script.md
```

---

## 🔗 相关 Skill

| Skill | 定位 | 仓库 |
|-------|------|------|
| [sa-pro-workbench](https://github.com/yinjianheng/sa-pro-workbench) | 解决方案架构师工作台 | 方案设计 · 架构图 · 投标 |
| [ba-workbench](https://github.com/yinjianheng/ba-workbench) | 商业分析工作台 | 战略分析 · 财务建模 · 商业论证 |
| [it-consulting-workbench](https://github.com/yinjianheng/it-consulting-workbench) | IT 咨询顾问工作台 | IT 战略 · 数字化转型 · 技术尽调 |

> 💡 **国际版**：[smart-procurement-navigator-international](https://github.com/yinjianheng/smart-procurement-navigator-international) — Dual-track China + Global bidding AI assistant

---

## 📄 许可证

**温馨提示**：本 Skill 为个人开源作品，仅供个人学习、研究及非商业用途。未经作者书面授权，严禁任何形式的商业使用（包括但不限于转售、捆绑销售、商业培训、SaaS化服务等）。作者已委托专业知识产权律师团队进行全网监测，侵权必究。

---

<p align="center">
  <b>👨‍💻 yinjianheng（殷健恒）</b> &nbsp;|&nbsp;
  📧 yinjianheng@foxmail.com &nbsp;|&nbsp;
  💬 WeChat: YJH-yinjianheng
</p>
<p align="center">
  <sub>⭐ 如果这个 Skill 帮到了你，请给个 Star 让更多人看到！</sub>
</p>