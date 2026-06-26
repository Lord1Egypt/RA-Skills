# Surgery-PMPH-10edition

<div align="center">

> *"21st Century Medical Student Guide"*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Skills](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)

<br>
> Clinical Skills Handbook Based on *Surgery, 10th Edition* (People's Medical Publishing House) — 240 Surgical & Critical Care Clinical Skills
<br>
<br>
<img src="https://github.com/xllgreen/Surgery-PMPH-10edition-/blob/main/assets/Surgery.png" width="260px">
<br>

Why struggle through a whole book?<br>
Just ask a question and get the solution directly from the textbook.

<br>

**Other Languages:**

[简体中文](README.md) · [日本語](README_JP.md) · [Français](README_FR.md) · [Русский](README_RU.md)

</div>

---

## About the Project

This project systematically integrates core domains including clinical surgery, critical care medicine, perioperative management, trauma care, comprehensive cancer treatment, infection control, and multi-system disease diagnosis and treatment. It covers **240 key clinical skills** organized into **17 major categories**.

**Target Audience**: Surgeons, Emergency Physicians, ICU Teams, Medical Students

**Reference Textbook**: *Surgery*, 10th Edition, People's Medical Publishing House

## Project Structure

```
Surgery-PMPH-10edition/
├── SKILL.md              # Core configuration — 240-skill registry
├── README.md             # This document — project overview & usage guide
├── <skill-name>/         # Detailed definitions for each skill
│   └── SKILL.md          #   Skill details (indications, steps, references)
├── scripts/              # Executable utility scripts
│   ├── skill-search.sh   #   Keyword-based skill search
│   └── skill-report.sh   #   Skill inventory report generator
├── config/               # Configuration files
│   └── skill-config.yaml #   Skill classification & metadata configuration
└── tests/                # Validation & testing
    └── validate-all.sh   #   Integrity validation script
```

## Skill Categories Overview

| Category | Skills | Description |
|----------|--------|-------------|
| 🚑 Emergency & Resuscitation | 14 | CPR, shock resuscitation, electrolyte disorder emergencies |
| 🦴 Trauma & Fractures | 27 | Fracture classification, reduction & fixation, nerve injuries |
| 🩺 General Surgery & Abdominal Emergencies | 22 | Appendicitis, intestinal obstruction, hernia, peritonitis |
| 🫁 Hepatobiliary-Pancreatic-Splenic Surgery | 19 | Biliary stones, pancreatitis, liver trauma |
| 🩻 Gastrointestinal Surgery | 10 | Gastric cancer, colorectal cancer, GERD |
| 🫘 Urology | 24 | Stones, tumors, infections, urethral injuries |
| 🩸 Vascular Surgery | 7 | DVT, varicose veins, vascular repair |
| 🔥 Burns & Plastic Surgery | 8 | Area estimation, depth classification, skin grafting |
| 🧬 Surgical Oncology & Comprehensive Treatment | 16 | TNM staging, radiotherapy/chemotherapy, limb-salvage surgery |
| 📋 Perioperative Management | 18 | Preoperative optimization, antibiotics, nutritional support |
| 💉 Anesthesiology & Pain Management | 11 | Airway management, spinal anesthesia, local anesthesia |
| ⚖️ Endocrinology & Metabolism | 6 | Hyperparathyroidism, dehydration, electrolyte disorders |
| 🦠 Infection & Immunology | 7 | Tuberculosis, sepsis, tetanus |
| 📡 Imaging & Interventional Radiology | 10 | Contrast imaging, endoscopy, interventional radiology |
| 🏋️ Rehabilitation & Functional Assessment | 12 | Fracture rehabilitation, neurological assessment |
| 🦿 Rheumatology & Spinal Disorders | 5 | Ankylosing spondylitis, spinal stenosis |
| 🔧 Other Specialty Skills | 10 | ARDS, AKI, defibrillation, etc. |

## Quick Start

### Installation

CLI:
```bash
openclaw skills install surgery-pmph-10edition
```

Prompt:
```bash
Before installing anything, inspect the ClawHub skill metadata and setup requirements.
If the skill asks you to install a third-party package or CLI, verify its source, maintainer, and package contents before running the install command.
Install the skill "Surgery-PMPH-10edition" (xllgreen/surgery-pmph-10edition) from ClawHub only after those checks pass.
Skill page: https://clawhub.ai/xllgreen/surgery-pmph-10edition
Keep the work scoped to this skill only.
After install, help me finish setup from verified skill metadata.
Use only the metadata you can verify from ClawHub; do not invent missing requirements.
Ask before making any broader environment changes.
```

### Post-Installation Usage

Tell the agent the following:
```bash
Before each response, please look up the relevant medical skill to confirm.
```

### Searching Skills

```bash
# Search by keyword
bash scripts/skill-search.sh appendicitis

# Generate skill inventory
bash scripts/skill-report.sh
```

### How to Use

Each skill contains four parts:
1. **Indications** — When to trigger this skill
2. **Procedure Steps** — Standardized operational workflow
3. **Precautions** — Contraindications & warnings
4. **References** — Detailed supplementary materials

### Query Strategies

#### 1. **Concept**
Question:
```bash
What is the concept of pancreatic pseudocyst in surgery?
```
Answer:
```bash
## Pancreatic Pseudocyst (PPC) — Concept
A pancreatic pseudocyst is a complication **following acute pancreatitis, pancreatic trauma, or chronic pancreatitis**. It is essentially **a cystic structure formed when pancreatic juice leaks through a necrotic or ruptured pancreatic duct and becomes encapsulated by fibrous tissue in the peripancreatic space or lesser sac**.
### Key Features
| Feature | Description |
|---------|-------------|
| **"Pseudo" meaning** | The cyst wall **lacks an epithelial cell lining** (unlike true cysts); it is composed of fibrous connective tissue and granulation tissue |
| **Formation mechanism** | Pancreatic duct rupture → pancreatic juice extravasation → surrounding tissue inflammatory response & encapsulation → gradual cyst wall maturation (requires **≥6 weeks**) |
| **Cyst fluid composition** | Rich in pancreatic enzymes (amylase/lipase), proteinaceous fluid |
| **Common locations** | Lesser sac, peripancreatic spaces |
### Natural History
- **<4 cm** cysts almost always resolve spontaneously
- **<5 cm** — about 50% resolve spontaneously
- **>6 cm or multiple** — spontaneous resolution unlikely; intervention evaluation needed
- Cyst wall maturation takes approximately **6 weeks**; internal drainage is only suitable after maturation
### Differential Diagnosis from True Cysts / Cystic Neoplasms
> On imaging, PPC can be confused with pancreatic cystic neoplasms (e.g., serous cystadenoma, mucinous cystadenoma, IPMN). PPC is distinguished by three key features: history of acute pancreatitis/trauma, absence of epithelial lining, and significantly elevated cyst fluid amylase.
Would you like me to elaborate on treatment strategies (observation vs. internal drainage vs. external drainage vs. resection)?
```

#### 2. **Clinical Case Analysis**
Question:
```bash
A 28-year-old female with 3 years of infertility presents with amenorrhea and galactorrhea for 6 months. Physical exam: normal appearance, galactorrhea present, normal fundus and visual fields. Serum prolactin 250 ng/mL. MRI reveals a 4mm×4mm low-signal area within the sella, 5mm from the optic nerve. What is the diagnosis and treatment plan?
```
Answer:
```bash
## Case Analysis
**Key Clues:**
| Item | Finding |
|------|---------|
| Patient | 28-year-old female |
| Chief complaint | **Amenorrhea + galactorrhea + infertility** (classic triad) |
| Serum PRL | **250 ng/mL** (normal < 25, markedly elevated) |
| MRI | **4mm × 4mm low-signal area** within sella (microadenoma < 10mm) |
| Visual fields/acuity | **Normal**, 5mm from optic nerve (no compression) |
### Diagnosis: Prolactin-secreting Pituitary Microadenoma
**Basis:**
- High PRL → inhibits GnRH → **amenorrhea-galactorrhea-infertility syndrome**
- 4mm tumor = microadenoma
- No visual field defects indicate no compression of the optic chiasm
### Treatment: Medical Therapy First, No Surgery Indicated
**First-line: Dopamine Receptor Agonists**
| Drug | Dosage | Advantage |
|------|--------|-----------|
| **Cabergoline** | 0.25–0.5 mg, 1–2 times/week | First choice, fewer side effects, convenient dosing |
| Bromocriptine | 1.25–5 mg, 2–3 times/day | Alternative, but nausea/dizziness more common |
**Expected Outcomes:**
- **Within weeks** → PRL normalizes → resumption of ovulatory menstruation, galactorrhea resolves
- **Months to a year** → significant tumor shrinkage (~80–90% effective)
**Why No Surgery?**
- Microadenomas are treated medically first — high efficacy, minimal trauma
- Transsphenoidal surgery is indicated for: drug resistance/intolerance, optic nerve compression symptoms, or suspicion of non-prolactinoma (e.g., non-functioning adenoma)
- This case: 5mm from optic nerve, normal visual fields — **no surgical indication**
### Follow-up
- Check PRL every 3–6 months after treatment
- Annual MRI after tumor shrinkage
- Once PRL normalizes, pregnancy planning is possible; requires combined obstetric-endocrine management
```
#### 3. **Exam Questions**
Question:
```bash
The most serious complication of lower extremity deep vein thrombosis is:
A. Superficial varicose veins of the lower extremity
B. Pulmonary embolism
C. Associated arterial spasm, limb ischemia
D. Lower extremity ulcer
E. Vena cava obstruction
```
Answer:
```bash
The answer is **B. Pulmonary embolism**
The most serious complication of lower extremity deep vein thrombosis (DVT) is **pulmonary embolism (PE)** — the thrombus dislodges and travels through the inferior vena cava → right atrium → right ventricle → pulmonary artery, potentially causing massive pulmonary infarction and sudden death.
- **A** Superficial varicose veins → a manifestation of chronic-phase collateral circulation in DVT, not a serious complication
- **C** Associated arterial spasm, limb ischemia → seen in Phlegmasia Cerulea Dolens-type DVT; serious but with much lower incidence than PE
- **D** Lower extremity ulcer → chronic-phase sequela, not the most serious
- **E** Vena cava obstruction → rare, usually the result of proximal extension of DVT
The most致命 threat to DVT patients is **thrombus dislodgement leading to pulmonary embolism**, which is precisely why acute DVT requires immediate anticoagulation and, when anticoagulation is contraindicated, placement of an inferior vena cava filter.
```

## About the Author

**Xiao Lv Lv (xllgreen)** — [xllgreen.github.io](https://xllgreen.github.io) — Medical Student at Jiujiang University College of Clinical Medicine · Tech Geek

## Technical Support

<br>
PDF2App Project: https://pdf2app.cn
<br>
Microsoft Visual Studio Code: https://code.visualstudio.com/
<br>
Claude Code for VS Code: https://claude.com/
© 2026 Anthropic PBC
<br>
<br>
<img src="https://cdn.deepseek.com/logo.png?x-image-process=image%2Fresize%2Cw_1920" width="130px">
<br>DeepSeek API: https://platform.deepseek.com/
© 2026 Hangzhou DeepSeek Artificial Intelligence Basic Technology Research Co., Ltd. All Rights Reserved
<br>
<br>
<img src="https://cdn.cnbj1.fds.api.mi-img.com/aife/mimo-blog-fe/doc_build/static/image/logo.99baaffe.png" width="130px">
<br>Xiaomi Mimo API: https://platform.xiaomimimo.com/
Copyright © 2010 - 2026 Xiaomi. All Rights Reserved
<br>

## License

The content of this project is compiled based on *Surgery*, 10th Edition (People's Medical Publishing House) and is provided for study and reference purposes only.

## Star History

<a href="https://www.star-history.com/?repos=xllgreen%2FSurgery-PMPH-10edition-&type=date&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=xllgreen/Surgery-PMPH-10edition-&type=date&theme=dark&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=xllgreen/Surgery-PMPH-10edition-&type=date&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=xllgreen/Surgery-PMPH-10edition-&type=date&legend=top-left" />
 </picture>
</a>
