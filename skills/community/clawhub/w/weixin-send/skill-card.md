## Description:

Sends proactive text messages to WeChat ClawBot users as a fallback when the native openclaw-weixin message tool is unavailable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luhuiwang](https://clawhub.ai/user/luhuiwang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to send proactive text-only WeChat notifications from OpenClaw agents, cron jobs, or external scripts when the normal openclaw-weixin message tool is unavailable or the active tool profile does not expose messaging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential-backed outbound WeChat messaging can be triggered by workflows that are allowed to execute the helper script.

Mitigation: Install only for trusted workflows, restrict access to the OpenClaw Weixin account directory, and treat script execution as equivalent to bot messaging permission.

Risk: The fallback path may not use the normal messaging permission profile or session logging path.

Mitigation: Prefer the native OpenClaw message tool whenever it is available, and use this skill only as a fallback with separate operational logging where required.

Risk: Configurable API base URLs can increase exposure if account configuration is untrusted or tampered with.

Mitigation: Use account files created by a trusted OpenClaw login flow and avoid configurable API base URLs unless they are strictly validated and trusted.

## Reference(s):

- [weixin-send ClawHub page](https://clawhub.ai/luhuiwang/skills/weixin-send)
- [Publisher profile](https://clawhub.ai/user/luhuiwang)
- [OpenClaw project](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with bash and Python snippets; the helper script emits JSON status objects.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Text-only WeChat messages; requires a locally logged-in openclaw-weixin account and recent context token for the target user.]

## Skill Version(s):

1.2.0 (source: server release metadata; artifact frontmatter says 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
