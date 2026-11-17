## Description:

Guides developers through preparing, uploading, validating, and archiving SkillHub.cn skill releases while separating public release packages from runtime secrets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawhub-master](https://clawhub.ai/user/clawhub-master)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill publishers use this guide to package a SkillHub.cn skill, publish it through the web interface or CLI, and verify that credentials and runtime-only files are not included in the release package.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports live-looking IMA credentials in the guide.

Mitigation: Do not reuse the embedded credentials; treat them as compromised, rotate them if they belong to you, and replace examples with environment-provided secrets.

Risk: The guide tells users to run local code with credentials and absolute local module paths.

Mitigation: Review code before execution, avoid loading modules from absolute local paths, and use an audited client with a pinned or project-local CLI install.

Risk: The guide includes cross-session notification behavior.

Mitigation: Send notifications only after explicit user confirmation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clawhub-master/skills/skillhub-upload-guide)
- [Publisher profile](https://clawhub.ai/user/clawhub-master)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with command examples and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes web and CLI publishing steps, release package checks, and security handling guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
