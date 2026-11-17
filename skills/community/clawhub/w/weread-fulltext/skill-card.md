## Description:

Exports books accessible through a logged-in WeRead account as Markdown with a source map and quality report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jes614753-sketch](https://clawhub.ai/user/jes614753-sketch)

### License/Terms of Use:

MIT-0

## Use Case:

WeRead users can export books they are authorized to access for personal, local reference. The skill captures rendered pages, reconstructs Markdown text, and records source and quality information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Whole-book exports may copy content beyond the user's rights.

Mitigation: Export only books and content you are authorized to copy and use.

Risk: A reusable WeRead login state and full book artifacts are stored locally.

Mitigation: Use a separate account or browser profile where appropriate, restrict local file access, and remove saved credentials and exports when no longer needed.

Risk: Browser automation may affect the WeRead account, and unpinned dependencies can change.

Mitigation: Review the skill before installing, consider a separate account for initial runs, and pin and review dependencies.

## Reference(s):

- [Weread Fulltext on ClawHub](https://clawhub.ai/jes614753-sketch/skills/weread-fulltext)
- [WeRead](https://weread.qq.com)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Files]

**Output Format:** [Markdown book text and quality report, JSON source map and run metadata, and captured page images]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Source mapping and a quality report support review; OCR and capture coverage do not guarantee complete or exact text.]

## Skill Version(s):

2.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
