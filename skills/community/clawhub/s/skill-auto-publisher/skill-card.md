## Description:

Helps agents publish ClawHub skills by checking slug availability, validating metadata, incrementing versions, generating changelogs, and running publish commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qianduoduo1422608857](https://clawhub.ai/user/qianduoduo1422608857)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to prepare and publish ClawHub skill releases with metadata validation, version updates, changelog support, and publication history tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The publishing helper can modify skill metadata and publish through local ClawHub credentials.

Mitigation: Use it only on trusted skill directories and review the release summary, metadata changes, and publish command before execution.

Risk: The documented confirmation step is not enforced by the publishing script.

Mitigation: Add a real confirmation or dry-run gate before allowing publication.

Risk: The publishing script contains a validated local code-execution bug in python3 -c interpolation.

Mitigation: Fix the interpolation bug before processing third-party or untrusted skills.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qianduoduo1422608857/skills/skill-auto-publisher)
- [Publisher profile](https://clawhub.ai/user/qianduoduo1422608857)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May modify skill metadata and publish through local ClawHub credentials when its publishing script is used.]

## Skill Version(s):

1.1.0 (source: server release evidence and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
