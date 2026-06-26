# Thesis Reviewer — Systematic Thesis Review for All Disciplines

[中文文档](README_CN.md)

An AI coding agent skill for systematically reviewing master's and doctoral theses across all academic disciplines. Provides full-spectrum, structured review feedback from a supervisor's perspective — designed to help students improve their thesis before submission.

## What it does

- Converts `.docx` thesis to Markdown via `markitdown` MCP, then reviews chapter by chapter
- **Supports all disciplines** with 7 discipline-specific review modules + universal framework
- **Supports both master's and PhD theses** — auto-detects degree type, adapts review standards
- **Academic vs professional degree** distinction per 2025 Degree Law
- **5 review dimensions**: academic quality, writing quality, formatting (GB/T 7713.1), data & results, academic integrity
- **Two-phase workflow**: Phase 1 auto deep analysis → Phase 2 interactive refinement
- **149 universal checklist items** + 22-34 discipline-specific supplements (170+ per review)
- **PhD-specific evaluation**: originality assessment, independent research capability, research system coherence, publication record
- **Blind review risk assessment**: predicts potential issues across 5 review dimensions
- **Severity markers**: 🔴 Serious / 🟡 Needs improvement / 🟢 Good — no ambiguous numeric scores
- **Cross-chapter consistency checks**: questions↔results, methods↔data, citations↔references
- **Prioritized revision roadmap** — students know exactly what to fix first
- **National standards aligned**: GB/T 7713.1-2006, GB/T 7714-2015, GB 3100-3102-93

## Multi-Platform Support

Works with all major AI coding agents that support the [Agent Skills](https://agentskills.io) format:

| Platform | Status | Details |
|----------|--------|---------|
| **Claude Code** | ✅ Full support | Native SKILL.md format |
| **OpenClaw / ClawHub** | ✅ Full support | `metadata.openclaw` namespace, dependency gating |
| **Hermes Agent** | ✅ Full support | `metadata.hermes` namespace, tags, category |
| **OpenAI Codex** | ✅ Full support | `agents/openai.yaml` sidecar file |
| **OpenCode** | ✅ Full support | SKILL.md auto-discovery |
| **Pi-Mono** | ✅ Full support | `metadata.pimo` namespace, tags |
| **SkillsMP** | ✅ Indexed | GitHub topics configured |

## Comparison

### vs No Skill (native agent)

| Feature | Native agent | This skill |
|---------|-------------|------------|
| Structured review framework | No — ad hoc, varies by run | Yes — 5 dimensions, 149 universal + discipline-specific items (170+ total) |
| Multi-discipline support | No — generic | Yes — 7 discipline-specific modules (life sciences, medicine, CS/AI, engineering, chemistry, physics, social sciences) |
| National standards aligned | No | Yes — GB/T 7713.1, GB/T 7714, GB 3100-3102 |
| Master's + PhD support | No — one-size-fits-all | Yes — adapts standards by degree level |
| Two-phase workflow | No — single-pass only | Yes — auto analysis + interactive refinement |
| Cross-chapter checks | No | Yes — questions↔results, methods↔data, citations↔references |
| PhD originality assessment | No | Yes — original contribution, independent research, system coherence |
| Severity markers | No — inconsistent feedback format | Yes — 🔴/🟡/🟢 with prioritized revision roadmap |
| Review report template | No — freeform output | Yes — formal review report deliverable to students |
| Life sciences expertise | Generic | Domain-specific (experimental design, statistics, nomenclature) |
| Interactive refinement | No — must re-prompt entirely | Yes — per-chapter discussion, adjust/add/remove opinions |
| .docx support | Limited | Yes — auto-converts via markitdown MCP |

## How it works

```
Input .docx
    │
    ▼
[Preprocessing] markitdown → Markdown → identify chapter structure
    │
    ▼
[Phase 1: Auto Deep Analysis]
    ├─ Step 1: Overall scan (structure, research question, global impression)
    ├─ Step 2: Chapter-by-chapter + global analysis (170+ checklist items)
    ├─ Step 2b: Cross-chapter consistency checks
    └─ Step 3: Generate draft review report
    │
    ▼
[Phase 2: Interactive Refinement]
    ├─ Discuss specific chapters in depth
    ├─ Ask follow-up questions about specific issues
    ├─ Adjust severity markers, add/remove opinions
    └─ User says "完成精修" to finalize
    │
    ▼
[Final] Merge all changes → save final review report as Markdown
```

## Review Dimensions

### 1. Academic Quality
Abstract, introduction/literature review, materials & methods, results, discussion, conclusion, innovation — with domain-specific checks for experimental design, sample size, controls, and biological replicates.

### 2. Writing Quality
Logical coherence between chapters, argumentative rigor (claim-evidence-reasoning), academic language standards, abstract quality (Chinese + English).

### 3. Formatting
Chapter completeness, figure/table standards (numbering, titles, resolution, three-line tables), reference format consistency, abbreviations, biological nomenclature (gene names in italics).

### 4. Data & Results
Appropriate chart types, error bars/confidence intervals, statistical test selection (parametric vs non-parametric), p-value notation, multiple comparison correction, figure quality (axis labels, legends, color-blind friendly), reproducibility.

### 5. Academic Integrity
Plagiarism detection, image manipulation, data fabrication, citation ethics, originality declaration completeness.

### Discipline-Specific Modules

| Module | Covers |
|--------|--------|
| **Life Sciences** | Experimental design (controls, replicates), reagent/instrument documentation, biological nomenclature (gene italics), data submission (GEO/SRA), Western blot/flow cytometry standards |
| **Medicine** | Clinical study design (CONSORT/STROBE), ethics (IRB, informed consent, ChiCTR registration), diagnostic test metrics, patient privacy |
| **Computer Science / AI** | Algorithm formalization, baseline comparison, ablation studies, data leakage prevention, code reproducibility, evaluation metrics |
| **Engineering** | Experimental apparatus documentation, simulation validation (mesh independence), measurement uncertainty, industry standards (GB/ISO/ASTM) |
| **Chemistry / Materials** | Synthesis documentation, characterization data (NMR/MS/XRD), IUPAC nomenclature, CCDC submission, safety protocols |
| **Physics** | Theoretical derivation rigor, experimental error analysis, numerical convergence, physical symbol conventions |
| **Social Sciences** | Questionnaire validity/reliability, sampling methodology, endogeneity control, qualitative coding transparency, value-fact distinction |

### PhD-Specific Dimensions (additional)
- **Originality**: original contribution vs incremental improvement, publishability at high-impact journals/conferences
- **Independent research capability**: ability to formulate questions, design research, diagnose problems
- **Research system coherence**: logical connections between multi-chapter studies, progressive depth
- **Literature review depth**: field-level understanding, coverage of classic and cutting-edge work, critical evaluation of debates
- **Publication record**: papers published/accepted during candidacy, relationship to thesis content

## Prerequisites

- `markitdown` MCP — required for `.docx` to Markdown conversion

## Skill Installation

### Claude Code

```bash
# Global install (available in all projects)
git clone https://github.com/Agents365-ai/thesis-reviewer.git ~/.claude/skills/thesis-reviewer

# Project-level install
git clone https://github.com/Agents365-ai/thesis-reviewer.git .claude/skills/thesis-reviewer
```

### OpenClaw / ClawHub

```bash
# Via ClawHub
clawhub install thesis-reviewer

# Manual install
git clone https://github.com/Agents365-ai/thesis-reviewer.git ~/.openclaw/skills/thesis-reviewer

# Project-level install
git clone https://github.com/Agents365-ai/thesis-reviewer.git skills/thesis-reviewer
```

### Hermes Agent

```bash
# Install under research category
git clone https://github.com/Agents365-ai/thesis-reviewer.git ~/.hermes/skills/research/thesis-reviewer
```

Or add an external directory in `~/.hermes/config.yaml`:

```yaml
skills:
  external_dirs:
    - ~/myskills/thesis-reviewer
```

### OpenAI Codex

```bash
# User-level install
git clone https://github.com/Agents365-ai/thesis-reviewer.git ~/.agents/skills/thesis-reviewer

# Project-level install
git clone https://github.com/Agents365-ai/thesis-reviewer.git .agents/skills/thesis-reviewer
```

### OpenCode

```bash
# Global install
git clone https://github.com/Agents365-ai/thesis-reviewer.git ~/.opencode/skills/thesis-reviewer
```

### Pi-Mono

```bash
# Global install
git clone https://github.com/Agents365-ai/thesis-reviewer.git ~/.pimo/skills/thesis-reviewer
```

### SkillsMP

```bash
skills install thesis-reviewer
```

### Installation paths summary

| Platform | Global path | Project path |
|----------|-------------|--------------|
| Claude Code | `~/.claude/skills/thesis-reviewer/` | `.claude/skills/thesis-reviewer/` |
| OpenClaw | `~/.openclaw/skills/thesis-reviewer/` | `skills/thesis-reviewer/` |
| Hermes Agent | `~/.hermes/skills/research/thesis-reviewer/` | Via `external_dirs` config |
| OpenAI Codex | `~/.agents/skills/thesis-reviewer/` | `.agents/skills/thesis-reviewer/` |
| OpenCode | `~/.opencode/skills/thesis-reviewer/` | — |
| Pi-Mono | `~/.pimo/skills/thesis-reviewer/` | — |

## Usage

Just provide your thesis file:

```
Review this master's thesis: /path/to/thesis.docx
```

Or in Chinese:

```
帮我评审这篇硕士论文：/path/to/thesis.docx
```

The skill will automatically convert, analyze, and generate a structured review report.

## Trigger Keywords

- Chinese: 论文评审, 学位论文, 审阅论文, 论文修改意见, 硕士论文, 博士论文, 毕业论文
- English: thesis review, dissertation review, thesis feedback, PhD thesis, doctoral thesis

## Output Files

| File | Description |
|------|-------------|
| `{filename}-converted.md` | Converted Markdown text |
| `{filename}-review-draft.md` | Phase 1 draft review report |
| `{filename}-review-final.md` | Final review report |

## Files

- `SKILL.md` — main skill instructions, loaded by all platforms
- `checklist.md` — universal review checklist across 5 dimensions (loaded by SKILL.md during review)
- `output-template.md` — review report output template (loaded by SKILL.md for report generation)
- `disciplines/` — discipline-specific review modules:
  - `life-sciences.md` — biology, biomedical, ecology, agriculture
  - `medicine.md` — clinical medicine, public health, pharmacy
  - `cs-ai.md` — computer science, AI, machine learning
  - `engineering.md` — mechanical, electrical, chemical, civil engineering
  - `chemistry.md` — chemistry, materials science
  - `physics.md` — theoretical, experimental, computational physics
  - `social-sciences.md` — economics, management, law, education, psychology
- `agents/openai.yaml` — OpenAI Codex-specific configuration
- `README.md` — this file (English, displayed on GitHub homepage)
- `README_CN.md` — Chinese documentation

> **Note:** `SKILL.md`, `checklist.md`, `output-template.md`, and `disciplines/` are needed for the skill to work. `agents/openai.yaml` is only needed for Codex. The README files are documentation only.

## Known Limitations

- **Requires markitdown MCP**: The skill depends on the `markitdown` MCP tool for `.docx` conversion. Without it, you must manually convert the thesis to Markdown first.
- **Long documents**: Very long theses (>80,000 words) may require multiple reading passes due to context window limits. The chapter-by-chapter approach mitigates this.
- **Formatting detection**: Some formatting issues (image resolution, page headers) cannot be fully detected from the Markdown conversion and may need manual checking.
- **Language**: Review output is in Simplified Chinese, designed for Chinese university thesis review workflows.

## License

MIT

## Support

If this skill helps you, consider supporting the author:

<table>
  <tr>
    <td align="center">
      <img src="https://raw.githubusercontent.com/Agents365-ai/images_payment/main/qrcode/wechat-pay.png" width="180" alt="WeChat Pay">
      <br>
      <b>WeChat Pay</b>
    </td>
    <td align="center">
      <img src="https://raw.githubusercontent.com/Agents365-ai/images_payment/main/qrcode/alipay.png" width="180" alt="Alipay">
      <br>
      <b>Alipay</b>
    </td>
    <td align="center">
      <img src="https://raw.githubusercontent.com/Agents365-ai/images_payment/main/qrcode/buymeacoffee.png" width="180" alt="Buy Me a Coffee">
      <br>
      <b>Buy Me a Coffee</b>
    </td>
  </tr>
</table>

## Author

**Agents365-ai**

- Bilibili: https://space.bilibili.com/441831884
- GitHub: https://github.com/Agents365-ai
