---
name: cs-math-research
description: >
  Use this skill to write complete, formatted academic graduation research papers and
  projects for the College of Computer Science and Mathematics at Tikrit University.
  Trigger whenever the user asks to write, create, generate, or produce a BSc graduation
  project, research paper, or academic document in computer science, mathematics,
  networking, artificial intelligence, machine learning, robotics, or any related field —
  especially when they mention Tikrit University, كلية علوم الحاسوب, or need a Word (.docx)
  output following Iraqi university standards. Also trigger when they mention chapter
  structure, abstract, literature review, methodology, or results sections for a CS paper.
  Always use this skill even if the user only mentions one part (e.g., "write the abstract"
  or "write Chapter One") — apply the full structure and conventions defined here.
---

# CS & Math Research Writing — Tikrit University

This skill captures the precise formatting, structure, language conventions, and
academic standards required for graduation research papers at the **College of Computer
Science and Mathematics, Tikrit University**, based on real documents produced in prior
sessions.

---

## 1. Document Identity & Cover Page

Every research document must open with this exact hierarchy of institutional identity:

```
Republic of Iraq
Ministry of Higher Education & Scientific Research
Tikrit University
College of Computer Science and Mathematics
[Department Name] Department
```

Followed by:
- **Research/Project Title** — centered, bold, 16pt+
- Submission line: *"Submitted to the [Department] Department, College of Computer
  Science and Mathematics, Tikrit University, in Partial Fulfillment of the Requirements
  for the Bachelor of Science Degree in [Field]"*
- **Prepared by:** [Student Name(s)] — in Arabic if the student is Iraqi
- **Supervised by:** [Supervisor Name with academic title, e.g., م.م. / أ.م.د.]
- Hijri year (e.g., 1446هـ) on the left, Gregorian year (e.g., 2025م) on the right

After the cover, insert:
1. **Bismillah page** — بسم الله الرحمن الرحيم with a Quranic verse (standard Iraqi academic tradition)
2. **Dedication page** — brief, heartfelt, addressed to family / mentors / friends
3. **Acknowledgment page** — 1–2 paragraphs thanking family, university, supervisor

---

## 2. Document Language Policy

| Section | Language |
|---|---|
| Cover page | English (with Arabic student name if applicable) |
| Bismillah / Dedication / Acknowledgment | Arabic |
| Abstract (English) | English |
| Abstract (Arabic — الخلاصة) | Arabic — always include both |
| All chapters (Introduction through Conclusions) | English |
| References | English (IEEE or APA style) |
| Table of Contents | English |

**Dual abstract is mandatory.** The Arabic abstract (الخلاصة) appears at the very end
of the document, after References.

---

## 3. Required Chapter Structure

Follow this five-chapter structure exactly:

### Chapter One: Introduction
- **1.1 Introduction** — Background of the field, motivation, real-world relevance
- **1.2 The Research Problem** — Clearly stated challenges (use bullet points for sub-problems)
- **1.3 The Research Aims / Objectives** — Numbered or bulleted list of specific goals
- **1.4 Related Work** — Brief paragraph-form survey of prior studies (3–6 references minimum)

### Chapter Two: Literature Review (Theoretical Background)
- In-depth exposition of all core technologies, algorithms, hardware, or theoretical
  concepts used in the project
- Each major component gets its own numbered subsection (2.1, 2.2, 2.3…)
- Include **figures** with captions ("Figure 2-X: Description") and **tables** where appropriate
- For hardware-based projects: include component specs and describe each part
- For AI/ML projects: explain the model architecture, training methodology, datasets

### Chapter Three: Research Methodology
- **3.1 Introduction** — Brief overview of what this chapter covers
- **3.2+** — Detailed subsections describing the system design, implementation phases,
  circuit diagrams, algorithms, datasets, software environment, etc.
- Include **phase-by-phase breakdown** if the project has multiple stages
- Include **cost table** (in IQD — Iraqi Dinars) for hardware projects:
  | NO | Device | Cost (IQD) |
- Include **system architecture diagram** or **flowchart** description

### Chapter Four: Results and Discussion
- **4.1 Introduction**
- **4.2+** — Present results with tables (accuracy metrics, performance data, etc.)
- Include comparison with prior related work
- Discuss challenges encountered and limitations

### Chapter Five: Conclusions
- Summary of what was achieved
- Key findings
- Future work recommendations (at least 3–5 concrete suggestions)

---

## 4. Figures and Tables

- **Figures** → numbered as: `Figure (Chapter-Number): Caption`
  Example: `Figure (2-3): Arduino UNO R3`
- **Tables** → numbered as: `Table Chapter-Number: Caption`
  Example: `Table 3-1: Circuit Components`
- All figures and tables must be referenced in-text before they appear
- A **Table of Figures** section follows the Table of Contents

---

## 5. References Format

Use **IEEE-style** numbered references. Examples:

```
[1] Author, A., & Author, B. Title of paper. Journal Name, vol(issue), pages, year.
[2] Author, C. Title of conference paper. In Conference Name, Publisher, year.
```

- Minimum **10–15 references** for a BSc project
- References appear at the end of the document, before the Arabic abstract
- In-text citations use square brackets: `[1]`, `[2, 3]`, `[16]`

---

## 6. Formatting Specifications (for .docx output)

When generating a Word document, apply these settings:

| Element | Specification |
|---|---|
| Font (English body) | Times New Roman, 12pt |
| Font (Arabic text) | Traditional Arabic or Times New Roman, 14pt |
| Line spacing | 1.5 lines |
| Margins | 2.5 cm all sides (or 1 inch) |
| Chapter headings | Bold, 14pt, centered |
| Section headings (1.1) | Bold, 12pt, left-aligned |
| Subsection headings (1.1.1) | Bold, 12pt, left-aligned |
| Page numbers | Bottom center, starting from Chapter One |
| Table of Contents | Auto-generated from heading styles |
| Cover page | No page number |
| Paper size | A4 |
| Arabic text direction | RTL (right-to-left) |

---

## 7. Common Project Types & Their Specific Conventions

### 7a. AI / Machine Learning Projects (CNN, YOLO, Deep Learning)
- Chapter Two must explain: neural network basics → specific architecture (CNN, YOLO, etc.)
  → dataset → training parameters → evaluation metrics
- Accuracy table format:
  | Metric | Value |
  | Precision | X% |
  | Recall | X% |
  | mAP@0.5 | X% |
- Mention: training/validation/test split percentages (e.g., 70/20/10)
- Mention: number of epochs, image size, batch size

### 7b. Robotics / Hardware Projects
- Must include: component list table (Name, Quantity, Specification)
- Must include: cost table in IQD
- Phases: Assembly → Embedded System → Control System → Sensors → Testing
- Describe: microcontroller model, motor drivers, power supply, communication modules
- Component figures are expected for each major hardware part

### 7c. Networking / Protocol Projects
- Chapter Two: OSI model → Transport Layer → TCP vs UDP comparison table
- Include: Three-Way Handshake explanation for TCP
- Include: socket programming concepts if implementation is included
- Compare your implementation against protocol standards

### 7d. Database / Information Systems
- Chapter Two: Database design principles → ER diagram → normalization
- Chapter Three: System design → database schema → interface screenshots
- Chapter Four: Testing scenarios and results table

### 7e. Signature / Image Processing / Pattern Recognition
- Chapter Two: Preprocessing → feature extraction → classifier architecture
- Chapter Three: Dataset description, augmentation techniques, model training
- Chapter Four: Confusion matrix, ROC curve description, accuracy metrics

---

## 8. Academic Writing Style Guidelines

- Write in **formal third-person academic English** ("The system demonstrates…",
  "The results indicate…", "This research presents…")
- Avoid first-person ("I built…" → "The researcher developed…")
- Each paragraph in Chapter One should end with at least one citation `[X]`
- Related Work section: describe each cited paper in 1–2 sentences, do not quote directly
- Conclusions must NOT introduce new information — only summarize findings
- Avoid contractions ("don't" → "do not", "can't" → "cannot")

---

## 9. Abstract Writing Formula

**English Abstract** (150–250 words):
1. What the project does (1–2 sentences)
2. The main technology/approach used
3. Key components or system architecture
4. Training/implementation details (if AI/hardware)
5. Results achieved (with numbers if available)
6. Significance / potential applications
7. Challenges identified

**Arabic Abstract (الخلاصة)** — mirror the English abstract translated into formal
Arabic. Place at the very end of the document after all references.

---

## 10. Dedication & Acknowledgment Templates

### Dedication (brief, 3–5 lines):
```
To Family
To Friends
To Mentors
To Loved Ones
```
Or a more personal version addressing specific people.

### Acknowledgment (1–2 paragraphs):
Express gratitude to: family → friends → university/department → supervisor →
professors. Mention the emotional and academic support provided. Formal but warm tone.

---

## 11. Supervisor Title Conventions (Iraqi Academia)

| Title | Meaning |
|---|---|
| م.م. | Mudarris Musa'id (Assistant Lecturer) |
| م. | Mudarris (Lecturer) |
| أ.م. | Ustaadh Musa'id (Assistant Professor) |
| أ.م.د. | Ustaadh Musa'id Doktor (Assistant Professor, PhD) |
| أ.د. | Ustaadh Doktor (Professor, PhD) |

Always include the supervisor's title before their name on the cover page.

---

## 12. Quality Checklist Before Finalizing

Before delivering the document, verify:

- [ ] Cover page has all institutional hierarchy (Republic → Ministry → University → College → Department)
- [ ] Bismillah page present
- [ ] Dedication and Acknowledgment in Arabic
- [ ] Table of Contents with correct page references
- [ ] Table of Figures included
- [ ] Both English and Arabic abstracts present
- [ ] All five chapters present with correct numbering (1.1, 1.2, etc.)
- [ ] All figures captioned and numbered correctly
- [ ] All tables captioned and numbered correctly
- [ ] References section with 10+ IEEE-style citations
- [ ] In-text citations throughout (especially Chapter One and Two)
- [ ] Arabic خلاصة at the very end
- [ ] Supervisor title is correct (م.م., أ.م.د., etc.)
- [ ] Hijri and Gregorian years on cover page
- [ ] File output is `.docx` format

---

## 13. Generating the .docx Output

When creating the Word document, **always read the docx SKILL.md first** at:
`/mnt/skills/public/docx/SKILL.md`

Use the `docx` Node.js library (not python-docx unless specifically requested).
Build the document programmatically, applying all formatting from Section 6 above.

Key structural order for the document builder:
1. Cover page (no page number)
2. Bismillah page
3. Dedication page
4. Acknowledgment page
5. Abstract (English)
6. Table of Contents
7. Table of Figures
8. Chapter One through Chapter Five
9. References
10. Arabic Abstract (الخلاصة)

---

## Reference Files

- `references/topic-templates.md` — Ready-made content outlines for common CS topics
  (smart home, robotics, CNN, networking, signature verification, etc.)
- `references/arabic-abstracts.md` — Arabic phrasing templates for common project types