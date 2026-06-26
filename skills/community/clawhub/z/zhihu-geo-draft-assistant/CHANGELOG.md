# Changelog

All notable changes to the `zhihu-geo-draft-assistant` Skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-05-12

### Added
- Initial release of the `zhihu-geo-draft-assistant` Skill.
- Created `SKILL.md` and `README.md` defining the explicit Human-in-the-loop and non-publishing scope.
- Added comprehensive `prompts/` for Zhihu-style rewriting (long answer, short answer, no-ad, article).
- Added `scripts/draft_to_zhihu.example.py` providing safe, headless=False Playwright drafting automation.
- Provided example input assets and output artifacts based on the "PowerMatrix/OpenClaw" use case.
- Integrated `automation/safety_rules.md` explicitly forbidding cookie theft, automated publishing, and API abuse.
