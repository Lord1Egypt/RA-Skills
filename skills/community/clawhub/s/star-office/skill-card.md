## Description:

Star Office helps an agent deploy a pixel-art office dashboard for multi-agent status visualization, mobile viewing, and public access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18153](https://clawhub.ai/user/18153)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agent users use this skill to launch and share a Star Office UI dashboard that shows agent work states, yesterday memos, multi-agent presence, and optional AI-generated room customization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public sharing and agent-sync endpoints can expose control of the dashboard or local activity when defaults are used.

Mitigation: Use only on localhost until default secrets are changed, sample join keys are removed, mutation and memo endpoints are disabled or authenticated, and the exact deployed code has been reviewed.

Risk: Remote downloaded push scripts may run unreviewed code in an agent environment.

Mitigation: Use an audited local copy of office-agent-push.py instead of running a remotely downloaded script.

Risk: Status details and yesterday memos can include private work information.

Mitigation: Curate status text and memo files before exposing the dashboard to other users or public networks.

Risk: Bundled or referenced art assets may have non-commercial restrictions separate from code license terms.

Mitigation: Replace art assets with original or fully licensed assets before commercial use.

## Reference(s):

- [Star Office ClawHub release](https://clawhub.ai/18153/skills/star-office)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [Star Office UI overview](docs/STAR_OFFICE_UI_OVERVIEW.md)
- [March 2026 changelog](docs/CHANGELOG_2026-03.md)
- [Desktop pet state API](desktop-pet/STATE_API.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup, deployment, status-sync, public-access, and security-hardening guidance for running the Star Office UI dashboard.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
