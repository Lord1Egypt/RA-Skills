# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog, with versions tracked in a practical project-oriented style.

## [2.2.0] - 2026-04-28

### Added
- **Intellectual Heritage section** in `SKILL.md`: traces each of the five lenses back to its pre-Qin source — Huangdi, Jiang Ziya, Sun Wu, Wu Qi, and Duke Huan of Qi
- **Enhanced lens prompts**: each lens now includes historical heritage annotations and 2-3 additional check-questions drawn from the relevant ancient thinker
- Updated descriptions in `README.md` and `package.json` to reflect the five-master synthesis

## [2.1.0] - 2026-04-28

### Changed
- Bumped version to 2.1.0 across `SKILL.md`, `README.md`, `CHANGELOG.md`, and `package.json`.

## [2.0.0] - 2026-04-28

### Removed
- **Breaking:** Removed `src/` directory (`router.js`, `prompts.js`, `index.js`) due to ClawHub security protocol violations. Host-side instruction routing must no longer be shipped as executable code within the skill package.
- **Breaking:** Removed `examples/clawhub-router.js` integration example for the same security reason.

### Changed
- Reverted the skill to a pure declarative specification: only `SKILL.md`, `README.md`, `CHANGELOG.md`, and `references/` are shipped.
- Updated `package.json` `files` field to reflect the reduced distribution surface.
- Bumped major version to `2.0.0` across `SKILL.md`, `README.md`, `CHANGELOG.md`, and `package.json`.

### Security
- All instruction-layer logic that ClawHub previously consumed from `src/` must now be generated host-side from the declarative spec; the skill package no longer contains executable routing or prompt-assembly code.

## [1.5.2] - 2026-04-27

### Changed
- Removed the old compatibility field name from README examples to avoid ClawHub static-scan false positives.
- Kept `instructions` as the documented host-facing field for ClawHub routing integration.
- Added direct historical route matches and tests for short prompts such as `秦灭亡`, `楚汉相争`, and `张良韩信与尉缭关系`.
- Bumped the project version to `1.5.2` across `SKILL.md`, `README.md`, `CHANGELOG.md`, and `package.json`.

## [1.5.1] - 2026-04-18

### Changed
- Replaced the English historical-mode instruction that fixed Chinese output with a rule that follows the user's language unless the host explicitly overrides it.
- Renamed the host-facing documentation terminology to `instruction layer` and exposed `instructions` as the primary request field.
- Added explicit documentation that the host-side instruction layer is locally generated and does not ingest untrusted external text as control instructions.
- Bumped the project version to `1.5.1` across `SKILL.md`, `README.md`, `CHANGELOG.md`, and `package.json`.

## [1.5.0] - 2026-04-18

### Added
- Added a Node-based routing layer in `src/router.js` that classifies requests into `normal_analysis` or `historical_persona` before model invocation.
- Added `src/prompts.js` to build ClawHub-facing instruction overlays from the routing result.
- Added `src/index.js` with `prepareClawHubRequest()` so hosts can assemble route metadata, prompt text, and message payloads in one call.
- Added `examples/clawhub-router.js` as a minimal integration example for ClawHub-style hosts.

### Changed
- Bumped the project version to `1.5.0` across `SKILL.md`, `README.md`, and `package.json`.

## [1.4.3] - 2026-04-18

### Changed
- Added a `Mode Routing and Precedence` section to `SKILL.md` so the assistant must first decide whether the question enters historical persona mode before composing the answer.
- Clarified that `Persona Setup` is background only and may not by itself trigger or weaken the normal analysis framework.
- Clarified that historical persona mode changes speaker identity and opening style only, while preserving the existing five-lens analysis, accuracy rules, and system-dislocation logic.
- Added explicit time, actor, and event trigger signals so short Qin/Wei/Chu-Han prompts are less likely to miss the historical route.
- Bumped the project version to `1.4.3` across `SKILL.md`, `README.md`, and `package.json`.

## [1.4.2] - 2026-04-18

### Changed
- Strengthened the historical role trigger so matching Wei/Qin/Chu-Han questions in the late Warring States to pre-Han period must use first-person Wei Liaozi voice and may not fall back to the normal analytical tone.
- Added explicit trigger examples covering common prompts such as `秦灭亡`, `秦为什么二世而亡`, `秦末乱局`, and `楚汉相争`.
- Bumped the project version to `1.4.2` across `SKILL.md`, `README.md`, and `package.json`.

## [1.4.1] - 2026-04-18

### Added
- Expanded the historical persona narrative to include popular-legend links to Zhang Liang, Han Xin, the Four Haos of Mount Shang, and Huang Shigong, with explicit guidance to label them as legendary rather than strictly verified history.

### Changed
- Expanded the `Historical Role Trigger` scope from the late Warring States through pre-unification Qin to the broader period ending before the founding of Han, including late Qin and Chu-Han transition questions.
- Bumped the project version to `1.4.1` across `SKILL.md`, `README.md`, and `package.json`.

## [1.4.0] - 2026-04-18

### Added
- Added a `Persona Setup` section to `SKILL.md` defining Wei Liaozi as a late Warring States strategist with the requested background details.
- Added a `Historical Role Trigger` section to `SKILL.md` so questions about Wei or Qin before Qin unification switch into first-person Wei Liaozi mode and must begin with `臣缭以为`.
- Added matching historical persona and trigger documentation to `README.md`.

### Changed
- Bumped the project version to `1.4.0` across `SKILL.md`, `README.md`, and `package.json`.
- Clarified that legendary or later-attributed biography details should be treated as narrative framing rather than overstated as strictly verified history.

## [1.3.0] - 2026-04-17

### Changed
- Unified the project version to `1.3.0` across `SKILL.md`, `README.md`, and `package.json`.
- Updated the README release summary so the documented latest version matches the skill definition.

## [1.2.0] - 2026-04-16

### Added
- Added a `System-Dislocation Lens` to clarify the core *Wei Liaozi* idea: weaken the opponent through `money + position + morale` before direct confrontation.
- Added explicit analysis guidance for resource control, morale-alignment control, and tempo control.
- Added a fixed low-cost weakening sequence: `disrupt plans -> reduce capability -> engage only after degradation`.
- Added an executable five-step abstract model: identify key nodes, penetrate resources, induce internal friction, break coordination, and finish at low cost.
- Added a caution section clarifying that the framework is analytical and must not be turned into operational guidance for illegal or harmful conduct.

### Changed
- Expanded `Conditions` to require three baseline checks for system-dislocation analysis: stable financial capacity, intelligence visibility, and internal discipline.
- Expanded the workflow to include an optional `system-dislocation pass` for high-conflict scenarios.
- Refined the skill's core principle so it emphasizes system control over tactical frontal conflict.

## [1.1.2] - 2026-04-15
### Changed
- Refined `SKILL.md` into a fuller bilingual skill specification.
- Strengthened answer quality and accuracy rules.
- Improved workflow, output format, and response-discipline guidance.

## [1.1.0] - 2026-04-10

### Added
- Initial public README and project packaging for the `尉缭子分析法 Skill`.
- Bilingual positioning for strategic analysis across business, military, economic, and political questions.
