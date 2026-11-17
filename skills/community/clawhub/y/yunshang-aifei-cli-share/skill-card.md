## Description:

Yunshang Aifei Cli Share provides a Python CLI and API client for Yunshang Aifei OA tasks, projects, reimbursements, personnel records, leads, and reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wanxin0911](https://clawhub.ai/user/wanxin0911)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations users can use this skill to query and update Yunshang Aifei OA records through CLI commands or Python API calls. It is intended for authenticated internal OA workflows such as checking tasks, projects, reimbursements, contracts, business opportunities, weekly reports, and creating task or comment records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access production OA accounts and perform write actions that may change business records.

Mitigation: Use a dedicated low-privilege OA account and require separate confirmation before running production write actions such as task creation or weekly-report comments.

Risk: Session tokens, OA credentials, and model-provider API keys could be exposed through local configuration or token storage.

Mitigation: Protect local .env and token files, use a dedicated model-provider key, rotate credentials regularly, and avoid sharing workspaces that contain cached tokens.

Risk: Transport or raw API usage could expose sensitive business, HR, or finance data or cause unintended operations.

Mitigation: Avoid raw API commands for routine use, restrict execution to trusted networks, and fix HTTPS transport plus protected token storage before handling sensitive data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wanxin0911/skills/yunshang-aifei-cli-share)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)
- [API catalog](artifact/api-catalog.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash, Python, JSON, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit CLI output for OA records and API responses; users must supply local credentials and environment configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
