## Description:

Helps agents search Toupiaoya voting templates, create and manage online voting projects, upload materials, and query voting or traffic data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jijun](https://clawhub.ai/user/jijun)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to find voting templates, create text, image, or video voting activities, upload materials, and inspect voting or visit data in Toupiaoya.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved authentication tokens may be sent to caller-controlled API endpoints if custom base URL or related environment overrides are used.

Mitigation: Use only trusted Toupiaoya endpoints and avoid custom --base-url or TOUPIAOYA_* API base overrides.

Risk: Authenticated commands can create or modify remote voting projects and upload local files.

Mitigation: Review project, option, group, and file inputs before execution, and do not upload sensitive local files.

Risk: The saved X-Openclaw-Token functions as account authority for Toupiaoya actions.

Mitigation: Protect ~/.toupiaoya/config.json, rotate the token if exposed, and remove it when no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jijun/skills/toupiaoya-creator)
- [Toupiaoya token access page](https://www.toupiaoya.com/skillAccess/token)
- [Toupiaoya create API endpoint](https://ai-api.toupiaoya.com/iaigc-toupiaoya/create)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands and JSON command responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save an X-Openclaw-Token locally, call Toupiaoya HTTP APIs, create or modify remote voting projects, and upload local files when invoked.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
