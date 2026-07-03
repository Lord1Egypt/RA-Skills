# 🏛️ Smart Procurement Navigator v2.0.0

[![Version](https://img.shields.io/badge/version-2.0.0-blue)](https://github.com/yinjianheng/smart-procurement-navigator-international)
[![License](https://img.shields.io/badge/license-Personal%20Use%20Only-red)](./LICENSE)
[![Author](https://img.shields.io/badge/author-yinjianheng-orange)](https://github.com/yinjianheng)
[![Platform](https://img.shields.io/badge/platform-WuKong%20%7C%20Claude%20%7C%20OpenClaw-brightgreen)](https://github.com/yinjianheng)

> **AI-Powered Bid & Tender Management Assistant | Opportunity Discovery → Bid Assessment → Proposal Writing → Compliance Review | 12-Step End-to-End Pipeline**
>
> Dual-track coverage: China Government Procurement Law & Bidding Law + International (World Bank, ADB, FIDIC, UNCITRAL) procurement frameworks

---

## 🎯 Why This Skill?

| Pain Point | Solution |
|------------|----------|
| 📄 Hundreds of pages in tender docs — hard to extract key info | **Intelligent Parsing**: Auto-extract qualification thresholds, evaluation criteria, disqualification clauses |
| 📊 Complex scoring systems — unclear where to focus effort | **Evaluation Model Builder**: Distinguish knock-out criteria vs. scoring items, map to response chapters |
| ✍️ Proposal writing takes weeks, quality varies wildly | **AI-Assisted Drafting**: Generate chapter drafts from evaluation criteria + technical specs |
| ⚠️ High rejection risk — one oversight can cost the entire bid | **Compliance Review**: 30+ common rejection causes auto-detected, pre-submission clearance |
| 📅 Multiple deadlines — easy to miss critical dates | **Deadline Alerts**: 20+ key timeline milestones auto-tracked |

---

## 🚀 Core Capability Matrix

| # | Stage | Capability | Output |
|---|-------|------------|--------|
| 1 | 🎯 Opportunity Identification | Smart parsing of procurement notices | Opportunity brief + deadline alerts |
| 2 | 📋 Bid Feasibility Assessment | 4-dimension evaluation: qualifications / track record / budget / competition | Bid feasibility report |
| 3 | 🔍 Document Interpretation | Extract qualification thresholds, evaluation methods, disqualification clauses | Structured interpretation report |
| 4 | 🗂️ Material Structuring | Procurement docs → searchable text | Structured knowledge base |
| 5 | 📊 Evaluation Modeling | Knock-out vs. scoring vs. objective scoring | Scoring model + response mapping |
| 6 | 📝 Task Decomposition | Material checklist + responsible person + deadline | Bid task checklist |
| 7 | 🏗️ Architecture Design | Pre-index + chapter outline + page planning | Response proposal architecture |
| 8 | ✍️ Draft Generation | Generate from evaluation items + technical specs | Chapter drafts |
| 9 | 🎨 Polish & Enhancement | De-template + chart placeholder index | Polished drafts |
| 10 | ✅ Compliance Review | Missing items / formatting / deviations / rejection risks | Compliance review report |
| 11 | 🔒 Final Submission Review | Consistency verification + seal/signature check | Final clearance checklist |
| 12 | 📚 Knowledge Reuse | Root cause analysis of wins/losses | Reusable material library |

---

## 🌍 International Procurement Coverage

| Framework | Coverage |
|-----------|----------|
| 🇨🇳 China | Government Procurement Law, Bidding and Tendering Law, 2024 State Council Doc No. 21 |
| 🌐 World Bank | Procurement Regulations for IPF Borrowers, Standard Procurement Documents (SPDs) |
| 🏦 ADB | Procurement Policy, Standard Bidding Documents |
| 🏗️ FIDIC | Red Book / Yellow Book / Silver Book contract conditions |
| 🇺🇳 UNCITRAL | Model Law on Public Procurement |
| 🇪🇺 EU | EU Public Procurement Directives (2014/24/EU) |
| 🇺🇸 US | FAR (Federal Acquisition Regulation), DFARS |

---

## 📦 Quick Start

```bash
# Install for WuKong / Claude / OpenClaw
cp -r smart-procurement-navigator-international ~/.claude/skills/

# Trigger: just describe your need
"Analyze this World Bank tender notice"
"Extract qualification requirements from this RFP"
"Build an evaluation model for this bid"
"Run a compliance review on my proposal"
```

---

## 🏆 Key Highlights

- **Dual-Track Compliance**: China procurement laws + international frameworks (World Bank, ADB, FIDIC, UNCITRAL, EU, US FAR)
- **Full Evaluation Methods**: Comprehensive Scoring (Fixed Score / Interval / Rank-Based) + Price Score Anomaly Detection
- **E-Procurement Ready**: Remote cross-location evaluation, e-signature CA mutual recognition
- **Rejection Prevention**: 30+ common rejection causes with avoidance strategies
- **Remedy Mechanisms**: Three-tier challenge/complaint/appeal system (7→15→60 day limits)
- **SME Preferences**: Consortium bidding, prequalification vs. post-qualification, double envelope

---

## 📁 File Structure

```
smart-procurement-navigator-international/
├── SKILL.md                    # Core skill file
├── README.md                   # This file
├── agent.yaml / system_prompt.md / workflows.md / runbook.md
├── skills/procurement_skills.yaml
├── knowledge/README.md
├── templates/                  # 7 professional templates
│   ├── opportunity_brief.md
│   ├── tender_analysis_report.md
│   ├── score_model.md
│   ├── response_outline.md
│   ├── service_scheme_structure.md
│   ├── review_report.md
│   └── consistency_check_report.md
├── test_cases/p0_demo_cases.md
└── demo/demo_script.md
```

---

## 🔗 Related Skills

| Skill | Focus | Repository |
|-------|-------|------------|
| [sa-pro-workbench-international](https://github.com/yinjianheng/sa-pro-workbench-international) | Solution Architect Workbench | Architecture · Diagrams · Bidding |
| [ba-workbench-international](https://github.com/yinjianheng/ba-workbench-international) | Business Analysis Workbench | Strategy · Financial Modeling · Business Case |
| [it-consulting-workbench-international](https://github.com/yinjianheng/it-consulting-workbench-international) | IT Consulting Workbench | IT Strategy · Digital Transformation · Tech DD |

> 💡 **Chinese Edition**: [smart-procurement-navigator](https://github.com/yinjianheng/smart-procurement-navigator) — China-focused bidding AI assistant

---

## 📄 License

**Notice**: This Skill is a personal open-source project for personal learning, research, and non-commercial use only. Any form of commercial use (including but not limited to resale, bundled sales, commercial training, SaaS-based services) is strictly prohibited without the author's written authorization. The author has retained a professional IP legal team for global monitoring; infringement will be prosecuted.

---

<p align="center">
  <b>👨‍💻 yinjianheng (Yin Jianheng)</b> &nbsp;|&nbsp;
  📧 yinjianheng@foxmail.com &nbsp;|&nbsp;
  💬 WeChat: YJH-yinjianheng
</p>
<p align="center">
  <sub>⭐ If this Skill helps you, please give it a Star to help others discover it!</sub>
</p>