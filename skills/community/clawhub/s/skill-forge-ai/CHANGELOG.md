# Changelog

All notable changes to this project will be documented in this file.

## [4.0.0] - 2026-06-12

### Added
- **Progressive Disclosure (渐进式披露)**: Iron Rule 3 upgraded from "150 lines" to "≤200 lines + 3-tier split (references/scripts/assets)"
- **Extended frontmatter**: allowed-tools / model / effort / metadata fields for precise tool permission and thinking depth control
- **scripts/ directory**: executable scripts for deterministic operations (checks, exports, batch processing)
- **assets/ directory**: templates, schemas, example files, output styles
- **6-layer validation pipeline**: Schema → Security (7 items) → Trigger test (5+3 real user queries) → Dogfood → Quantitative scoring (0-10) → Baseline comparison (with vs without Skill)
- **Troubleshooting module**: optional 5th module in SKILL.md format (common errors + causes + solutions)
- **Real user trigger test**: 5 positive + 3 negative real user phrasings (including colloquial, rewritten, vague expressions)

### Changed
- Iron Rule 3: "150行以内" → "渐进式披露 (≤200行 + references/scripts/assets 三级拆分)"
- SKILL.md format: 4 modules → 4+1 modules (troubleshooting optional)
- Step 4b: "3正向+3反向假问题" → "5条真实用户说法+3条反向测试"
- Step 4: added Step 4d (quantitative scoring 0-10) and Step 4e (baseline comparison)
- Tencent 9-dimension #9: "under 150 lines" → "under 200 lines + progressive disclosure"
- Directory structure: references/ only → references/ + scripts/ + assets/

### Removed
- Hard 150-line limit (replaced by 200-line + progressive disclosure)

## [3.6.0] - 2026-06-12

### Changed
- Standardized trigger words: 技能熔炉 / 技能评估(skill评估,评估技能) / 技能发布(发布技能)
- Removed redundant triggers (熔炉创建/锻造技能/新建熔炉/熔炉技能/推送技能/发布到GitHub/发布到ClawHub)
- skill-publisher trigger words aligned: 技能发布/发布技能 only

## [3.5.0] - 2026-06-12

### Added
- Three-entry trigger system: 技能熔炉(full pipeline) / 技能评估(evaluation only) / 技能发布(publishing only)
- Phase 3: Publishing to GitHub + ClawHub (from skill-publisher, now integrated)
- Entry detection logic: trigger word determines which Phase to start from
- references/publishing-guide.md: merged from skill-publisher (repo structure + security audit + publish procedures)
- skill-publisher as independent lightweight entry for "发布技能" trigger

### Changed
- Description rewritten with three trigger word groups for three scenarios
- Title changed from "技能熔炉 v3.4" to "技能熔炉 v3.5"
- Phase 2 now also serves as standalone "技能评估" entry
- SKILL.md structure: 4 phases (0→1→2→3) instead of 3 phases (0→1→2)

## [3.4.0] - 2026-06-11

### Added
- Chinese trigger words: 技能熔炉/熔炉创建/锻造技能/新建熔炉/熔炉技能 — completely separates from built-in skill-creator
- "何时触发" section with explicit trigger word list and anti-confusion rules
- Bilingual description: Chinese trigger keywords front-loaded for reliable auto-triggering

### Changed
- Title changed from "Skill Forge" to "技能熔炉" — Chinese-first branding
- Description rewritten: Chinese trigger words first, English Do NOT scope preserved
- All section headers translated to Chinese for consistency
- Version bumped from v3.3 to v3.4

## [3.3.0] - 2026-06-07

### Added
- Security Red Line Check (Step 4a+1): 7-item security scan before delivery
- Do NOT scope in description: "Do NOT use for editing existing skills, skill security vetting, or general coding tasks."

### Changed
- Refined self-validation pipeline: Schema → Security → Trigger → Dogfood
- Improved Phase 2 benchmarking flow with clearer user decision options

## [3.2.0] - 2026-06-06

### Added
- Phase 2: SkillHub Peer Benchmarking — search, rank, and compare against Top 3 peers
- Tencent 9-dimension compliance comparison template
- Quality ranking formula: downloads × 0.4 + installs × 0.3 + stars × 0.3
- Differentiation & gap analysis with Tencent Manual justification
- Progressive Disclosure: moved detailed docs to references/ directory
- benchmarking-guide.md reference

### Changed
- SKILL.md trimmed from 319 lines to ~170 lines (detailed content moved to references/)
- Interview flow extracted to references/interview-flow.md
- Interview methods extracted to references/interview-methods.md

## [3.1.0] - 2026-06-05

### Added
- Adaptive 2-5 round interview (up from fixed 3 rounds)
- B1-B6 interview rules: behavioral probing, Why×1-2, bias detection, contradiction writeback, option-first 3+1, creative option probe
- Recursive search pattern: broad → deepen → precision → verify
- 3-step self-validation: Schema check → Trigger test → Dogfood simulation
- Convergence check after each interview round
- interview-flow.md and interview-methods.md references

### Changed
- Phase 0 intent recognition: element check before deciding interview vs direct creation
- Interview rounds now adaptive based on element convergence

## [3.0.0] - 2026-06-04

### Added
- Phase 0: Intent Recognition — detect whether context is sufficient or interview is needed
- 3-round structured interview for new skill creation
- Element checklist: single scenario / trigger condition / output format / scope boundary / hard constraints

### Changed
- Restructured from flat flow to phased pipeline (Phase 0 → Phase 1)

## [2.0.0] - 2026-06-03

### Added
- Three Iron Rules: Description-first / One-Skill-One-Job / Under 150 lines
- 4-module SKILL.md format: 任务/输出格式/规则/示例
- Useless rule filter: delete "语言简洁"/"保持客观"/"排版整齐" etc.
- Intern Test for rules: if an intern can't execute it, delete it

### Changed
- Complete rewrite from v1 template-based approach to rule-driven approach

## [1.0.0] - 2026-06-01

### Added
- Initial release: basic skill creation template
- SKILL.md frontmatter with name and description
- Simple creation flow without interview or validation
