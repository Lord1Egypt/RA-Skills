## Description:

Queries Baidu Qianfan Coding Plan usage and quota, with optional browser-assisted login when saved cookies are missing or expired.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wsjwoods](https://clawhub.ai/user/wsjwoods)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers who use Baidu Qianfan Coding Plan can use this skill to check short-term, weekly, and monthly quota consumption from an authenticated local session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reusable Baidu login cookies are saved locally in ~/.baidu-qianfan-auth.json.

Mitigation: Run the skill only on a trusted single-user machine, restrict access to the cookie file, and delete it when quota checks are no longer needed.

Risk: Selected Baidu cookies are sent to the Qianfan quota endpoint during quota checks.

Mitigation: Use the skill only for the intended Baidu Qianfan account and review the endpoint and request behavior before installation.

Risk: Automatic login depends on agent-browser interacting with the Baidu login flow.

Mitigation: Review the agent-browser dependency and prefer manual review of login steps before relying on automatic browser actions.

## Reference(s):

- [Qianfan Usage ClawHub page](https://clawhub.ai/wsjwoods/skills/qianfan-usage)
- [Qianfan Usage README](artifact/README.md)
- [agent-browser dependency](https://github.com/nicepkg/agent-browser)
- [Baidu Qianfan quota endpoint](https://console.bce.baidu.com/api/qianfan/charge/codingPlan/quota)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Terminal text output with quota totals, reset times, status messages, and setup commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Baidu session cookies saved locally after login and sends selected Baidu cookies to the Qianfan quota endpoint.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
