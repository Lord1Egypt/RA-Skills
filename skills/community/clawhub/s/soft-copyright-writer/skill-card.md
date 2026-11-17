## Description:

Guides users through Chinese software copyright registration material preparation, including information intake, material checklists, source-code formatting, design document drafting, application-form guidance, and pre-submission checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, founders, enterprises, and IP support staff use this skill to prepare Chinese software copyright registration materials for individual, enterprise, or joint applications. It helps structure required information, draft supporting documents, format source-code excerpts, and check consistency before submission.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Users may provide sensitive source code, identity documents, signatures, company seals, or business registration details while preparing application materials.

Mitigation: Provide only the information needed for the task, redact secrets from code, and avoid sharing scans or official documents through untrusted channels.

Risk: Source-code excerpts may include hardcoded credentials, third-party libraries, or open-source code that should not be submitted as original core code.

Mitigation: Review source code before formatting, remove secrets, and exclude vendor, framework, generated, and non-original code.

Risk: Application guidance may become stale or may not match a user's specific legal or submission situation.

Mitigation: Verify final requirements and submission steps against the official copyright registration portal before filing.

## Reference(s):

- [Application Form Guide](references/application-form-guide.md)
- [Classification Codes](references/classification-codes.md)
- [Common Rejections](references/common-rejections.md)
- [Design Document Template](references/design-doc-template.md)
- [Material Checklist](references/material-checklist.md)
- [Source Code Format](references/source-code-format.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Chinese Markdown with tables, checkboxes, structured document drafts, and formatted source-code text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include formatted excerpts of user-provided source code and application material drafts.]

## Skill Version(s):

1.0.1 (source: frontmatter and server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
