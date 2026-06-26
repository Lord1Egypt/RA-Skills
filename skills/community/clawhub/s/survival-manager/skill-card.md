## Description: <br>
Survival Manager helps an agent monitor operating health, balance-driven survival levels, authorization requests, and finance logs while reserving high-risk actions for user approval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fffdz](https://clawhub.ai/user/fffdz) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External agent operators use this skill to keep an autonomous assistant within budget, monitor recurring operational checks, track income and expenses, and route risky actions through an authorization queue. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide autonomous activity involving financial records, account-visible data, browser-visible data, messaging services, and model or API spend. <br>
Mitigation: Review before installing, enable only integrations intended for use, and keep approval requirements active for sensitive operations. <br>
Risk: Broad operational instructions may allow file writes, external messages, subagent creation, or configuration changes without enough scoping. <br>
Mitigation: Require explicit user approval before those actions and record decisions through the authorization queue. <br>
Risk: The documentation references scripts and automation behavior that should not be trusted unless included and separately reviewed. <br>
Mitigation: Do not run referenced scripts or automation steps until their contents are present in the release artifact and have been reviewed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/fffdz/survival-manager) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown reports, authorization request text, finance log entries, configuration snippets, and PowerShell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or update local operational files such as authorization queues, finance logs, and survival configuration when the user approves.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
