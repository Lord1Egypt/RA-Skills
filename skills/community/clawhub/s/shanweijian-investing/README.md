# shanweijian-investing

**Apply the distilled investing philosophy and negotiation principles of Shan Weijian (单伟建) to real decisions.**

This is a [Codex/Agent Skill](https://github.com/openai/codex) built from the original texts of Shan Weijian's three books — *Out of the Gobi*, *Money Games*, and *Money Man* — plus his public writings and interviews (2021-2026). Everything is distilled directly from primary sources: no book reviews, no second-hand summaries.

---

## 中英双语说明 / Bilingual Guide

### 中文

本 skill 是一个「人物思想蒸馏」系统：把单伟建三本著作（约 75 万字原文）和近年公开言论，蒸馏成约 2.6MB、90 万字的结构化知识库。

**三本原著：**
1. 《走出戈壁》— 从文革失学到沃顿教授再到投资家的人格根基
2. 《金钱博弈》— 1997-1998 亚洲金融危机中收购韩国第一银行
3. 《金钱风云》— 2002-2004 收购深圳发展银行（中国首例外资控股全国性银行）

**知识库结构：**
```
SKILL.md                          主路由（使用入口）
references/
├── investing-principles.md       跨书综合原则（15条方法论）
├── synthesis/
│   └── cross-book-map.md         跨书印证体系（10大主题的逻辑中枢）
├── framework/
│   ├── deal-screening-system.md  五环投资筛选体系（打分卡+否决清单）
│   └── voice-samples.md          文风范例（分析报告/评论文章）
├── chapters/                     三本书逐章深蒸馏（1.0MB）
├── quotes/                       三本金句库（6600+句，带标签）
├── observations/                 观点库（1862条编号观点+出处）
└── dimensions/                   四大维度专题
    ├── life-decisions.md         人生抉择（27原则）
    ├── management-legal.md       企业管理/项目/法务（30原则）
    ├── people-judgment.md        识人与信任（27原则）
    ├── banking.md                银行业认知（40原则）
    └── public-statements.md      公开言论库（万达/恒大/人民币/TFP/AI）
```

**使用方法（Codex 桌面版）：**
1. 把整个文件夹放到 `~/.codex/skills/shanweijian-investing/`
2. 直接问：「用单伟建的思维分析这个交易/这个人/这个行业」
3. Agent 会按 SKILL.md 的路由自动调用对应文件

**核心方法论（五环筛选器）：**
- 环1 现金流独立性 30% ——「离了谁还能活」
- 环2 安全边际 25% ——「两三折的清算价」
- 环3 可切割性 20% ——「外科手术式切割」
- 环4 治理可修复性 15% ——「问题在股东，不在资产」
- 环5 退出预埋 10% ——「买之前先想怎么卖」

四个实战案例已用此体系打分示范：万达 8.5 / 恒大物业 7.6 / 平安集团 8.0 / 平安银行 7.2。

### English

This skill is a **person-thought-distillation system**: Shan Weijian's three books (~750K Chinese characters of original text) and recent public statements, distilled into a ~2.6MB structured knowledge base.

**The three books:**
1. *Out of the Gobi* — his personal foundation: from the Gobi desert during the Cultural Revolution to Wharton professor to investor
2. *Money Games* — acquiring Korea First Bank during the 1997-98 Asian financial crisis
3. *Money Man* — acquiring Shenzhen Development Bank (the first and only foreign-controlled national bank in China's history)

**What's inside:** chapter-by-chapter deep distillations, 6,600+ sourced quotes, 1,862 numbered viewpoints with provenance, four thematic dimension files, a five-ring deal-screening system, cross-book synthesis maps, and a voice-style guide for writing analyses in his tone.

**Usage (Codex desktop):** drop the folder into `~/.codex/skills/`, then ask things like "How would Shan Weijian analyze this deal?" The agent routes automatically via SKILL.md.

**The Five-Ring Screening System:**
1. Cash-flow independence (30%) — "Can it live without its parent?"
2. Margin of safety (25%) — "Buy at thirty cents on the dollar"
3. Separability (20%) — "Surgically cut toxic from clean"
4. Fixability of governance (15%) — "The problem is the shareholder, not the asset"
5. Exit pre-wiring (10%) — "Know how you'll sell before you buy"

Four real deals scored as worked examples: Wanda 8.5, Evergrande Property 7.6, Ping An Group 8.0, Ping An Bank 7.2.

---

## Sources & Methodology

- **Books**: user-provided licensed ebooks (epub/mobi/azw3 direct extraction + Tesseract OCR for image PDFs). All quotes are verbatim OCR, including typos, for authenticity.
- **Public statements**: 13 sourced articles (2021-2026) including interface news (Evergrande deal), Financial Times (RMB revaluation), Harvard Business Review, Caixin interviews, and Shan's signed essays. Each claim is tagged with source level (full-text vs snippet).
- **No fabrication rule**: every principle in the skill carries an observation ID or chapter reference. Content not in the sources is never invented; model-imitated voice samples are explicitly labeled.

## Stats

| Metric | Value |
|--------|-------|
| Total size | ~2.6 MB |
| Source text distilled | ~750K characters (3 books) + 13 articles |
| Sourced quotes | 6,600+ |
| Numbered viewpoints | 1,862 |
| Chapter units covered | 79 (all chapters + appendices + afterwords) |
| Thematic dimensions | 4 + public statements |
| Worked deal examples | 4 (Wanda, Evergrande Property, Ping An Group, Ping An Bank) |

## License

Content derived from Shan Weijian's copyrighted books is for personal research/education use. Book copyrights remain with the author and publishers (CITIC Press etc.). The distillation structure and analysis are open-sourced under MIT for the skill framework; original book text excerpts retain all rights.

## Disclaimer

This project is for research and education. It is not investment advice. Deal scores are illustrative applications of a distilled methodology, not recommendations.
