## Description:

Safely publish skills to ClawHub by sanitizing, formatting, verifying, and publishing without modifying local source files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and skill authors use this skill to prepare existing instructions or local skill content for public ClawHub release. It guides transformation into a publishable structure, sanitization of sensitive details, user approval, and post-publish checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing selected content can expose sensitive, personal, or internal information.

Mitigation: Review the generated publish folder carefully and confirm the sanitization checklist before any public release.

Risk: Using an unpinned npx publish command can introduce supply-chain uncertainty.

Mitigation: Prefer a pinned or preinstalled trusted ClawHub CLI version when publishing.

## Reference(s):

- [Skill Publish on ClawHub](https://clawhub.ai/ivangdavila/skills/skill-publish)
- [Sanitization Checklist](artifact/sanitize.md)
- [Transforming Content to Skill Format](artifact/transform.md)
- [Pre-Publish Verification](artifact/verify.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with checklists and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill directs the agent to create separate publish-ready files and to obtain explicit user approval before publishing.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
