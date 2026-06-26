# Changelog

All notable changes to `token-efficient-task-router` should be recorded in this file.

The format is intentionally lightweight:

- `MAJOR` for breaking routing or safety behavior changes
- `MINOR` for new capabilities or meaningful rule expansions
- `PATCH` for documentation, examples, tests, or small non-breaking fixes

## v0.6.8 - 2026-05-02

### Changed

- expanded Chinese and English README installation sections with WorkBuddy, CodeBuddy, and QClaw guidance
- public install guidance now distinguishes UI import, user-level directory install, project-level install, and OpenClaw-compatible fallback paths
- release artifacts now target `v0.6.8`

### Notes

- this patch improves platform installation guidance only and does not change skill behavior

## v0.6.7 - 2026-05-02

### Added

- split public guide into a Chinese `GUIDE.md` and an English `GUIDE.en.md`
- bidirectional language-switch links at the top of both guide files

### Changed

- README public document links now point to separate Chinese and English guide pages
- release artifacts now target `v0.6.7`

### Notes

- this patch improves public reading experience only and does not change skill behavior

## v0.6.6 - 2026-05-02

### Added

- split public repository homepage into a Chinese `README.md` and an English `README.en.md`
- bidirectional language-switch links at the top of both README files

### Changed

- README presentation now follows a clearer bilingual-repository pattern instead of mixed-language paragraphs
- release artifacts now target `v0.6.6`

### Notes

- this patch improves public reading experience only and does not change skill behavior

## v0.6.5 - 2026-05-02

### Changed

- README is now Chinese-first with English support, better aligned with Chinese-speaking public readers
- public-facing wording now fits GitHub and platform listings without changing skill behavior
- release artifacts now target `v0.6.5`

### Notes

- this patch is documentation-only and does not change routing logic or safety behavior

## v0.6.4 - 2026-04-29

### Added

- public repository `LICENSE`
- public repository `.gitignore`

### Changed

- README front section is now better suited for a GitHub repository homepage
- validation and publish checklist now cover public repository essentials
- release artifacts now target `v0.6.4`

### Notes

- this patch prepares the skill for cleaner open-source style repository publishing

## v0.6.3 - 2026-04-29

### Added

- public-facing `GUIDE.md` for external readers on GitHub, SkillHub, and ClawHub
- package-external maintainer playbook for local iteration and release handling

### Changed

- README has been rewritten as a release-facing overview instead of a maintainer-facing working note
- internal maintenance guidance is no longer intended to live inside the published skill package
- release artifacts now target `v0.6.3`

### Notes

- this patch separates public documentation from private maintenance workflow
- packaged users should only see release-facing material

## v0.6.2 - 2026-04-29

### Added

- Codex local-install guidance in the README for placing the skill under `~/.codex/skills`

### Changed

- README version references now point to `v0.6.2`
- release notes now record the local-install and finalization pass as a traceable patch

### Notes

- this patch closes the remaining packaging-to-installation gap for local Codex usage
- recommended release artifacts now use `v0.6.2`

## v0.6.1 - 2026-04-29

### Added

- platform quick commands reference for copy-ready prompts across CodeBuddy, WorkBuddy, iMA Copilot, and generic chat
- khazix skill pairing example for `hv-analysis`, `khazix-writer`, and `neat-freak`

### Changed

- README now includes a short command handbook and installed-skill pairing guidance
- SKILL.md now points to quick-start command prompts
- tests and checklist now verify quick-command and skill-pairing coverage

### Notes

- this is a cleanup-oriented patch release focused on easier real-world onboarding
- recommended release artifacts now use `v0.6.1`

## v0.6.0 - 2026-04-29

### Added

- CodeBuddy adaptation rules for read budget, edit budget, test budget, and staged refactor control
- CodeBuddy scope confirmation template
- CodeBuddy bugfix and refactor examples

### Changed

- WorkBuddy adaptation now includes file-scope budgeting and sample-batch-first handling
- focus activation can now select a `codebuddy-code` bundle
- README, tests, and validation rules now cover CodeBuddy and stronger WorkBuddy token-control behavior

### Notes

- this version makes the skill more portable across code-heavy and file-heavy agent products
- recommended release artifacts now use `v0.6.0`

## v0.5.0 - 2026-04-29

### Added

- platform-neutral chat confirmation affordance rules for button-ready, chip-ready, and quick-reply-friendly prompts
- button-ready confirmation template
- button-guided chat example

### Changed

- interactive routing, need calibration, and iMA runtime prompts now support button-ready option blocks
- the skill now explicitly prefers short choice sets over long confirmation paragraphs when user input is needed
- README, tests, and validation rules now include button-friendly confirmation behavior

### Notes

- this version improves the practical usability of the skill inside chat-based products where users confirm by tapping or sending short replies
- recommended release artifacts now use `v0.5.0`

## v0.4.0 - 2026-04-29

### Added

- real-need calibration rules for identifying whether the user truly needs a decision, sample, staged plan, or full delivery
- progressive delivery rules for choosing between decision-only, sample, staged execution, and full batch
- need calibration template
- need calibration example

### Changed

- the skill now treats non-essential token spending as something to avoid explicitly
- large-scope tasks now default to calibration and progressive delivery before full expansion
- focus activation can now select a `need-calibration` bundle
- iMA runtime guidance now includes full-vs-sample calibration behavior
- README, tests, and validation rules now reflect the new logic

### Notes

- this version strengthens the skill from a pure router into a real token-consumption control framework
- recommended release artifacts now use `v0.4.0`

## v0.3.0 - 2026-04-29

### Added

- iMA Copilot low-token runtime protocol
- iMA understanding lock sentence and one-screen first-turn rule
- iMA compact follow-up controls such as `1继续`, `2展开`, `3换模式`, `4只结论`, `5只列材料`
- focus activation rules to prevent loading too much of the skill before the task is precisely scoped
- focus selection template
- iMA lite response template
- focus activation and iMA lite examples

### Changed

- iMA Copilot adaptation is now more operational and chat-runtime aware
- the skill now explicitly chooses the smallest active capability bundle before loading detailed mode references
- README, tests, validator, and packager now reflect the new iMA and focus-activation behavior

### Notes

- this version targets real-world iMA Copilot token waste and skill-drift problems
- recommended release artifacts now use `v0.3.0`

## v0.2.0 - 2026-04-29

### Added

- initial publishable skill package structure
- Ask / Plan / Craft / Expert mode system
- risk levels, token budget modes, and token saving protocol
- file safety rules and ambiguity handling rules
- WorkBuddy and iMA Copilot adaptation guidance
- Interactive Routing Prompt mechanism
- full and lightweight routing confirmation templates
- quick reply code system such as `MPS`, `SPM`, and `2B`
- WorkBuddy file-safety confirmation prompt
- iMA knowledge-scope confirmation prompt
- local validation and packaging scripts

### Changed

- standardized the skill as a reusable SkillHub / ClawHub-ready package
- made routing behavior confirmation-aware for ambiguous and high-cost tasks

### Notes

- this is the first versioned release
- recommended packaging names now include the version number
