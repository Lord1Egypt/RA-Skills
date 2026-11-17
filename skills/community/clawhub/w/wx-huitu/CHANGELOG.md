# Changelog

All notable changes to this project will be documented in this file.

## [2.2.0] - 2026-07-14

### Security Hardening (SkillSpector Findings Fix)
- **Vague Triggers fix**: Removed overly broad triggers ("画图", "做个图"), added precise "公众号图表". Description and workflow.md and README synced.
- **Cloud sync gating**: Feishu cloud sync changed from default-on to opt-in (requires explicit user confirmation). Description, SKILL.md, workflow.md, README (CN+EN) all updated.
- **Chrome detection ordering**: Fixed-path detection now primary, registry query demoted to fallback. Added security note explaining --no-sandbox is a Puppeteer headless technical requirement, not privilege escalation.
- **User warnings strengthened**: README (CN+EN) restructured to separate default actions (local file write/subprocess/network) from optional actions (cloud upload). Explicit data-egress warning added.

## [2.1.0] - 2026-07-13

### Added
- SkillHub frontmatter fields (slug/displayName/version/summary/license)
- Permission declaration section in SKILL.md
- Bilingual README with user warnings
- Updated .gitignore with Python cache and ClawHub exclusions

## [2.0.0] - 2026-06-15

### Added
- Three canvas system (landscape 640x400 / standard 640x480 / square 640x640)
- 18 chart types with C01-C18 version IDs and CSS class names
- Chart version lock rule: data charts must use C01-C18
- Font size inverse ladder (larger=thinner, smaller=bolder)
- Semantic color variables (--good/--bad/--warn)
- KPI card + Sparkline component
- Three financial media color schemes (McKinsey/Economist/Caixin)
- 8 interception rules for inappropriate chart choices

## [1.0.0] - 2026-06-12

### Added
- Initial release of wx-huitu
- 14 chart types with HTML+CSS+SVG skeletons
- Three-axis decision framework (variable type x argument intent x data shape)
- 8 interception rules for inappropriate chart choices
- Okabe-Ito colorblind-safe palette with redundant encoding
- 4-step workflow: profile → recommend → generate → deliver
- Puppeteer-core screenshot delivery with Feishu cloud sync
- Two format sizes: landscape (640xauto) and square (640x640)
