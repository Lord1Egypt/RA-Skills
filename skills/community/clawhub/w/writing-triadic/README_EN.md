# Writing Triadic — Self-Evolving 3-Role Collaborative Writing Skill

> Writing is not a one-shot AI generation task. It needs **deep intent understanding**, **precise execution**, and **authentic reader feedback**.  
> v2.9.1 adds protocol reliability: a session state contract and adaptive 100-point scoring. v2.9 SEO, v2.8 Style Cloning, Long-Form Chapter Management, Template #16 Thesis Proposal, v2.7 Instant Mode, v2.6 Multi-Modal Iteration, and v2.5 Intelligent Blends are all retained.

## ✨ Core Philosophy

Writing Triadic decomposes writing into three roles plus an evolution engine:

| Role | Name | Responsibility |
|---|---|---|
| 🧠 **Creator** | Content Architect | Mines intent, matches templates, coordinates agents, supervises delivery, drives evolution |
| ✍️ **Executor** | Precision Writer | Produces drafts with meaningful divergence, dual-temperature writing, diff edits, and v3 synthesis |
| 👁️ **Reader** | Soul Audience | Inhabits the target reader persona, uses adaptive 100-point scoring, and selects the strongest version |
| 🧬 **Evolution Analyst** | Evolution Analyst v2 | Extracts preferences, corrections, style drift, adoption rate, vocabulary heatmaps, and veto signals |

## 🆕 v2.9.1 Highlights (2026-06-08)

### 🧩 Protocol Reliability Patch

- **New `session-state.md` contract**: records mode, template, blend, active modules, phase status, and decision log
- **New `references/state-contract.md`**: defines required artifacts, role handoffs, and failure handling
- **Adaptive Reader scoring**: SEO and style-clone dimensions redistribute weights; the base score always remains 100
- **Executor constraint warnings**: word count, SEO, style, and historical taboo conflicts must be reported instead of silently ignored
- **Cleaner evolution attribution**: SEO preferences go to the SEO archive; style-clone signals go to the style archive

## 🆕 v2.9 Highlights (2026-05-21)

### 🔎 SEO Content Optimization Module

- **6 subsystems**: keyword extraction, search intent classification, title scoring, density presets, readability targets, internal linking
- **New Phase 1.6**: runs after research and before rule-making when SEO applies
- **Phase 3 SEO checklist**: title, keywords, meta, structure, readability, internal links
- **Expanded template support**: #1 Technical Documentation, #2 Blog Post, #5 Business/Product Copy, #11 Product Manual/Tutorial Guide, #15 Product Review
- **Skip rules**: private writing, internal reports, fiction/essays, WeChat Moments, or explicit "no SEO"

### Reference Updates

- `references/seo-module.md` adds the full SEO protocol.
- `references/template-library.md` now includes SEO notes for every SEO-supported template.

## Retained Highlights

### v2.8

- **Style Cloning Engine**: 8-D fingerprint extraction, calibration dialog, dual-temperature injection, drift tracking, multi-profile support
- **Long-Form Chapter Manager**: Chapter Manifest, consistency watchdog, cross-session resume, chapter-level evolution
- **Template #16 Thesis Proposal**: background, literature review, objectives, method, innovation, schedule, references
- **Cold-Start Bootstrap**: asks two preference-probing questions for a new writing type

### v2.7

- **Instant Mode**: at most two lightweight question rounds, then direct output
- **Dual-temp writing**: high creativity pass plus low-temperature calibration
- **AI-trace quick scan**: forbidden items, fatigue words, length, passive voice, cliche ending

### v2.6

- **Mode A Diff-Modify**: edit only specified paragraphs
- **Mode B v3 Feature Synthesis**: merge the best parts of v1 and v2
- **Mode C Full Rewrite**: restart from rules when tone/structure changes heavily

### v2.5

- **Intelligent Blend Matching**: Recommend+Confirm → Default+Adjustable → Auto-Apply
- **Evolution Engine v2**: preference drift, veto rules, adoption rate, vocabulary heatmap

## 🚀 Quick Start

### Installation

```bash
openclaw skills install writing-triadic
```

### Usage

Just say what you want to write:

- "Write a blog post about AI coding assistants"
- "Draft product launch copy"
- "Write my performance review"
- "Start a sci-fi story"
- "Optimize my resume"
- "Write a WeChat Moments post"

### Workflow

```text
User request
    ↓
Phase 0: Read style evolution archive
    ↓
Phase 0.5: Style cloning entry, if a sample is provided
    ↓
Phase 1: Creator mines intent
    ↓
Phase 1 enhanced: intelligent blend recommendation
    ↓
Phase 1.5: Web research + knowledge base update
    ↓
Phase 1.6: SEO analysis, when public publishing + SEO-supported template apply
    ↓
Phase 2: Template matching (16 choose 1) + rules with history injection
    ↓
Phase 3: Executor produces drafts
    ↓
Phase 4: Reader evaluates as the target audience
    ↓
Phase 5: Creator presents final draft and handles corrections
    ↓
Phase 5.5: Evolution Analyst updates memory and statistics
```

## 📚 Supported Writing Types (v2.9.1 — 16 Templates)

| Category | Template Skeleton |
|---|---|
| Technical Documentation | TL;DR → Prerequisites → Step-by-Step → Gotchas |
| Blog Post | Hook → Why It Matters → Body → Actionable Takeaway → CTA |
| Personal Essay | Micro Detail → Associative Drift → Inner Conflict → Open Ending |
| Academic / Industry Paper | Abstract → Introduction → Methodology → Findings → Limitations |
| Business Copy | Problem → Agitation → Solution → Proof → CTA |
| Narrative Fiction | Inciting Incident → Rising Action → Climax → Resolution |
| Social Short | Title Hook → Persona Anchor → Point-by-Point → Tags + Engagement |
| Video Script / Voiceover | 0-3s Hook → Value Promise → Progressive Points → CTA |
| Email / Business Letter | Subject Line → Core Message → Details → Closing |
| Speech / Presentation | Opening Bomb → Body Expansion → Emotional Peak → Memorable Close |
| Product Manual | Safety Warning → Quick Start → Detailed Ops → Troubleshooting |
| Thesis / Dissertation | Introduction → Lit Review → Methodology → Results → Discussion → Conclusion |
| Resume / CV | Header → Objective → Education → Experience → Projects → Skills |
| WeChat Moments | Hook → Narrative Body → Emotional Landing |
| Product Review | Verdict → Quick Specs → Deep Experience → Comparison → Buying Advice |
| Thesis Proposal | Background → Literature → Objectives → Method → Innovation → Schedule → References |

## 🛡️ AI Trace Detection

The skill includes a full AI-trace avoidance guide covering high-risk words, structural cliches, hollow-content signals, bilingual cross-contamination, and user-specific historical taboos.

## 🔧 Model Configuration

| Role | Default Model | Rationale |
|---|---|---|
| Creator | `deepseek/deepseek-v4-pro` | Deep reasoning and quality control |
| Executor | `deepseek/deepseek-v4-flash` | Fast multi-draft generation |
| Reader | `deepseek/deepseek-v4-pro` | Critical evaluation |
| Evolution Analyst v2 | `deepseek/deepseek-v4-pro` | Preference judgment and global statistics |

Custom modes include all-Pro, all-Flash, and local Ollama privacy mode. See [references/model-config.md](references/model-config.md).

## 📁 File Structure

```text
writing-triadic/
├── SKILL.md                         # Main skill file (v2.9.1)
├── README.md                        # Chinese README
├── README_EN.md                     # This file
├── CHANGELOG.md                     # Update log
├── LICENSE                          # MIT License
├── skills-spring-roadmap.md         # Version roadmap
└── references/
    ├── creator-prompt.md            # Creator protocol
    ├── executor-prompt.md           # Executor prompt
    ├── reader-prompt.md             # Reader prompt with adaptive scoring
    ├── evolution-analyst-prompt.md  # Evolution Analyst protocol
    ├── template-library.md          # 16 templates + blends + SEO notes
    ├── style-cloning-guide.md       # Style cloning guide
    ├── ai-traces-guide.md           # AI trace avoidance guide
    ├── examples.md                  # End-to-end examples
    ├── seo-module.md                # SEO Content Optimization Module
    ├── state-contract.md            # Session state and handoff contract
    ├── instant-mode-protocol.md     # Instant Mode protocol
    ├── long-form-protocol.md        # Long-form chapter protocol
    ├── inkos-insights.md            # InkOS-inspired design notes
    └── model-config.md              # Model configuration reference
```

## 📄 License

[MIT](LICENSE) — Copyright (c) 2026 sallyface0

## 📝 Changelog

See [CHANGELOG.md](CHANGELOG.md).
