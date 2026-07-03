# Psychiatry Psychiatry-PMPH-9edition

<div align="center">

> *「21st Century Medical Student Guide」*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Skills](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)

<br>

> A clinical skill manual based on the 9th edition of *Psychiatry* (People's Medical Publishing House) — **47 Core Psychiatry Clinical Skills**

<br>

Why read a whole textbook?<br>
Just ask a question, and get the solution directly from the textbook.

<br>

**Other Languages:**

[中文](README.md) · [日本語](README_JP.md) · [Français](README_FR.md) · [Русский](README_RU.md)

</div>

---

## Introduction

This project systematically integrates comprehensive knowledge and practical guidelines across psychiatry, clinical psychology, and psychiatric rehabilitation, covering **47 key clinical skills** organized into 8 major categories: basic assessment and diagnostic research, mood/anxiety/OCD disorders, schizophrenia and psychotic disorders, neurocognitive and geriatric psychiatry, somatic/eating/sleep/substance use disorders, personality/development/trauma/dissociative disorders, emergency/crisis intervention and forensic ethics, and rehabilitation/community/integrated care.

**Target Audience**: Psychiatrists, psychotherapists, medical students, community mental health workers, consultation-liaison teams

**Reference Textbook**: People's Medical Publishing House *Psychiatry* 9th Edition

**⚠️ Risk Warning ⚠️**: This skill covers psychiatric diagnosis, pharmacotherapy, crisis intervention, forensic assessment, and rehabilitation management, which could be misused as independent medical advice.

**Mitigation**: Use output only as educational or clinician-reviewed reference material. Always verify recommendations against current official guidelines, local protocols, and qualified psychiatric specialists.

## Project Structure

```
psychiatry-pmph-9edition/
├── SKILL.md                    # Core configuration — 47-skill registry
├── README.md                   # This document — project overview and usage guide
├── README_EN.md                # English version
├── README_JP.md                # Japanese version
├── README_FR.md                # French version
├── README_RU.md                # Russian version
├── <skill-name>/               # Individual skill directories
│   ├── SKILL.md                #   Skill details (when to use, workflow, notes, references)
│   └── references/             #   Detailed reference materials (optional)
│       └── *.md
├── .clawhubignore              # ClawHub publish ignore rules
└── .gitignore                  # Git ignore rules
```

## Skill Categories

| Category | Skills | Description |
|----------|--------|-------------|
| 🧪 Basic Assessment & Diagnostic Research | 4 | Clinical assessment, diagnostic reasoning, classification, RDoC framework |
| 💚 Mood, Anxiety & OCD Disorders | 5 | Depression, bipolar, anxiety, OCD and related disorders |
| 🧠 Schizophrenia & Psychotic Disorders | 3 | Schizophrenia spectrum, severe mental illness, thought disorders |
| 🧓 Neurocognitive & Geriatric Psychiatry | 6 | AD, dementia screening, DLB, delirium, CLP |
| 🫁 Somatic, Eating, Sleep & Substance Use | 11 | Eating disorders, ARFID, BDD, sleep disorders, substance use |
| 👤 Personality, Development, Trauma & Dissociation | 6 | PD, neurodevelopmental, tics, PTSD, dissociative, perinatal |
| 🚑 Emergency, Crisis & Forensic Ethics | 5 | Crisis intervention, involuntary treatment, forensic evaluation, ethics |
| 🏥 Rehabilitation, Community & Integrated Care | 7 | Community rehab, ISP, inpatient training, prevention, pharmacotherapy |

> Full 47-skill details: see [SKILL.md](SKILL.md)

## Quick Start

### Installation

CLI:
```bash
openclaw skills install psychiatry-pmph-9edition
```

### Usage

Each sub-skill contains four sections:
1. **When to Use** — Trigger conditions
2. **Workflow** — Standard operating procedures
3. **Key Decision Points** — Important cautions and constraints
4. **References** — Detailed supplementary materials

## License

This project is compiled based on PMPH *Psychiatry* 9th Edition for educational reference only. Released under MIT-0 license.
