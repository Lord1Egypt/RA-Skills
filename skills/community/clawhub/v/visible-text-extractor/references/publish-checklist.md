# publish-checklist

## Before publishing

- Ensure `SKILL.md` has:
  - `name`
  - `description`
  - `version`
  - `metadata.openclaw`
- Ensure generated artifacts are excluded with `.clawhubignore`
- Ensure scripts referenced from `SKILL.md` actually exist
- Ensure the one-step deliverable pipeline still works end to end
- Ensure the skill package validates with the official package script

## Release expectations

A release-quality version of this skill should:
- produce readable output without requiring users to inspect raw OCR
- clearly state environment limits
- provide one-step Word generation
- separate audit data from end-user deliverables

## Suggested release notes for 1.0.0

- Initial public release
- Added one-step deliverable pipeline for clean markdown + Word output
- Added OCR cleanup and section reconstruction workflow
- Added troubleshooting and product-positioning docs
- Improved WeChat / screenshot / image-heavy page handling
