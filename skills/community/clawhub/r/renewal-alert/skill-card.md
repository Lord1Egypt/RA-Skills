## Description: <br>
Track insurance policy renewal dates and send timely reminders before policies expire. Use when users want to register insurance renewal dates, get expiry alerts, or review policies due for renewal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiwenbing](https://clawhub.ai/user/jiwenbing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to record insurance policy renewal details, receive reminders before expiry, and review upcoming renewals before coverage lapses or auto-renews. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incorrect renewal dates, policy details, or reminder timing could cause a user to miss coverage review or renewal. <br>
Mitigation: Ask the user to verify policy numbers, renewal dates, premium amounts, and reminder schedules against their insurer documents before relying on alerts. <br>
Risk: Renewal guidance may be mistaken for a definitive insurance recommendation. <br>
Mitigation: Frame renewal prompts as review support and advise users to confirm coverage decisions with their insurer or a qualified advisor. <br>
Risk: The release evidence security guidance is inconsistent with the artifact behavior. <br>
Mitigation: Treat evidence.security as the authoritative scan source while relying on artifact behavior only for renewal-alert-specific operational mitigations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiwenbing/renewal-alert) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration instructions] <br>
**Output Format:** [Markdown guidance with structured reminder details and renewal review prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No executable code, credentials, account access, or external tool calls are present in the artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
