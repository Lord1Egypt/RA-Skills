## Description:

Control, diagnose, or repair a visible Windows 11 Edge/Chrome browser from OpenClaw running in WSL2 via CDP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pe4atnik](https://clawhub.ai/user/pe4atnik)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to connect OpenClaw running in WSL2 to a visible Windows 11 Edge or Chrome browser for assisted browsing, diagnostics, and repair. It is intended for human-in-the-loop browser work that needs existing tabs, cookies, logins, CDP access, or manual handling of login, captcha, 2FA, approvals, and file dialogs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CDP access can expose control of a visible logged-in browser profile.

Mitigation: Prefer a dedicated browser profile, use personal or logged-in profiles only after explicit approval, and keep the browser visible for human oversight.

Risk: A WSL-visible CDP relay can be dangerous if reachable from the LAN or Internet.

Mitigation: Require confirmation before firewall or portproxy changes, scope Windows firewall rules to the WSL/Hyper-V CIDR, and verify the relay is not exposed beyond the intended local environment.

Risk: State-changing browser, account, payment, form, firewall, profile, config, or Scheduled Task actions may have persistent effects.

Mitigation: State the action, location, risk, and rollback before proceeding, then wait for explicit user confirmation.

Risk: The browser budget helper can print full page URLs, which may reveal sensitive browsing context.

Mitigation: Avoid running the helper on sensitive tabs unless full URL disclosure is acceptable or URLs are redacted before sharing.

## Reference(s):

- [Win11 Visible Browser on ClawHub](https://clawhub.ai/pe4atnik/skills/win11-visible-browser)
- [Setup reference](references/setup.md)
- [README](README.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell and PowerShell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include diagnostic steps, configuration recommendations, rollback notes, and browser/CDP evidence summaries.]

## Skill Version(s):

1.0.3 (source: server release metadata, _meta.json, and CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
