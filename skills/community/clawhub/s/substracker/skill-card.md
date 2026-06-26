## Description: <br>
SubsTracker manages subscriptions and configuration through CLI scripts for login, subscription CRUD, payment history, notifications, and dashboard queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ianchenx](https://clawhub.ai/user/ianchenx) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to manage a SubsTracker instance from an agent session, including subscription records, renewals, payment history, dashboard summaries, and notification settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses SubsTracker account credentials and notification secrets. <br>
Mitigation: Store SUBSTRACKER_* and notification values only in a protected configuration source and avoid passing secrets through casual prompts or untrusted directories. <br>
Risk: The skill persists a session cookie and can connect to whichever SubsTracker URL is configured. <br>
Mitigation: Use the skill only with trusted SubsTracker servers and clear the saved cookie when changing servers or rotating credentials. <br>
Risk: The skill can delete subscriptions or payments and update account, password, and notification configuration. <br>
Mitigation: Require explicit user confirmation before destructive actions, password changes, configuration updates, or notification tests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ianchenx/substracker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries and shell commands, with JSON returned by the SubsTracker CLI scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include subscription, payment, dashboard, and configuration data returned from the user's configured SubsTracker server.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
