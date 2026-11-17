## Description:

Export installed OpenClaw skills into shareable ZIP archives, detecting and staging external runtime files and generating install documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seph1709](https://clawhub.ai/user/seph1709)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to package installed skills for sharing or migration, with external runtime files staged and documented after user review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can package broad local directories or sensitive files into a ZIP archive.

Mitigation: Review every external file path before approving packaging, and avoid broad directories, credential stores, .env files, SSH keys, cloud config, package-registry tokens, logs, or personal documents unless they are intentionally being shared.

Risk: Credentials, tokens, and sensitive configuration are copied as real values when included.

Mitigation: Remove, redact, or replace sensitive values before sharing any generated archive.

Risk: A generated ZIP may contain private local data even though the skill does not transmit files itself.

Mitigation: Treat generated archives as sensitive artifacts and control distribution accordingly.

## Reference(s):

- [Skill Extractor ClawHub listing](https://clawhub.ai/seph1709/skills/skill-extractor)
- [Publisher profile](https://clawhub.ai/user/seph1709)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance, confirmation prompts, generated STRUCTURE.md content, and local ZIP archive paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local staging folders, _external/ contents, STRUCTURE.md, and a ZIP archive after user confirmation.]

## Skill Version(s):

1.8.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
