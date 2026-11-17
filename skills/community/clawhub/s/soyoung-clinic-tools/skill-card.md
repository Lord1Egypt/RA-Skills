## Description:

Soyoung Clinic Tools is an OpenClaw skill for Soyoung clinic workflows including appointment booking, store lookup, doctor information, schedules, project knowledge, and pricing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[east5ringroad-kyle](https://clawhub.ai/user/east5ringroad-kyle)

### License/Terms of Use:

MIT-0

## Use Case:

External users and clinic support agents use this skill to configure a Soyoung API key, find stores, check appointment slots, book or manage appointments, and retrieve Soyoung project, product, doctor, and schedule information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes an agent-startup hook that can influence future Soyoung-related agent sessions.

Mitigation: Review the hook before installation and enable it only when the workspace expects Soyoung clinic routing behavior.

Risk: Credential handling weaknesses were flagged by the authoritative security summary and guidance.

Mitigation: Configure API keys only in private chat, keep custom API URLs disabled unless the destination is trusted, and rotate keys if exposure is suspected.

Risk: Local state may contain identity, location, and appointment metadata.

Mitigation: Install only in appropriate workspaces, avoid sharing workspace state, and remove local state during uninstall or when access is no longer needed.

## Reference(s):

- [Soyoung API key login](https://www.soyoung.com/loginOpenClaw)
- [Soyoung Skill API specification](references/api-spec.md)
- [User guide](使用说明.md)
- [Changelog](CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text with inline shell command guidance and script-returned text or JSON summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires workspace message context and a Soyoung API key for authenticated appointment, project, and doctor workflows.]

## Skill Version(s):

2.2.2 (source: evidence.release.version, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
