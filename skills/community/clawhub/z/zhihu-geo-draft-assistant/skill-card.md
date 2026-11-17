## Description:

Transforms AI-GEO brand materials into Zhihu-style questions, answers, article drafts, titles, tags, and review checklists, with optional visible-browser draft filling for human review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ljseeking](https://clawhub.ai/user/ljseeking)

### License/Terms of Use:

MIT-0

## Use Case:

Brand teams, founders, and AI-GEO operators use this skill to convert brand profiles, FAQs, keyword matrices, and source drafts into Zhihu-ready Q&A and article content. The skill supports manual review and optional local browser-assisted draft filling without automated publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The content workflow can reduce or remove brand disclosure in a way that may violate Zhihu rules or mislead readers.

Mitigation: Require human review of sponsorship, affiliation, and marketing intent before drafting or publishing; do not use the no-ad prompt to hide material brand involvement.

Risk: Browser automation interacts with a logged-in Zhihu session and could affect account trust if expanded or misused.

Mitigation: Run Playwright locally in visible mode, keep dependencies pinned in an isolated environment, do not save credentials or session state, and keep publishing decisions manual.

Risk: Generated claims, examples, tags, and positioning may be inaccurate, overbroad, or unsuitable for the target account.

Mitigation: Use the generated publishing checklist to verify facts, boundaries, brand exposure, platform fit, and final responsibility before saving or publishing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ljseeking/skills/zhihu-geo-draft-assistant)
- [Artifact README](artifact/README.md)
- [Artifact Skill Definition](artifact/SKILL.md)
- [Automation Safety Rules](artifact/automation/safety_rules.md)
- [Playwright Draft Flow](artifact/automation/playwright_draft_flow.md)
- [Changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown drafts, prompt outputs, review checklists, templates, and Python/Playwright workflow guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces human-reviewed Zhihu draft assets and optional visible-browser draft filling; final editing, saving, and publishing remain manual.]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact CHANGELOG, released 2026-05-12)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
