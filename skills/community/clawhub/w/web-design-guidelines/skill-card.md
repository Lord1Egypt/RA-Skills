## Description:

Audits UI code and deployed pages against interface guidelines and Lighthouse targets, then documents evidence-backed findings for review and planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[afonsoft](https://clawhub.ai/user/afonsoft)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review UI code or measure deployed pages, document cited accessibility and performance findings, and plan approved fixes through specifications and issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running an unpinned Lighthouse command can fetch unexpected tool versions.

Mitigation: Pin the Lighthouse version before running checks against deployed URLs.

Risk: Generated specifications and issues can drive unintended downstream changes.

Mitigation: Review the findings and draft specifications, and explicitly approve issue creation and handoff before downstream work.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/afonsoft/skills/web-design-guidelines)
- [Publisher-provided project link (unverified)](https://github.com/afonsoft/skills)
- [Interface review guidelines](references/interface-guidelines.md)
- [Lighthouse verification workflow](references/lighthouse-verification.md)
- [Review report template](references/report-template.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown review reports and draft specifications; optional GitHub issues after approval]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source locations or Lighthouse audit evidence; user interactions are in Portuguese and written artifacts are in English.]

## Skill Version(s):

1.0.0 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
