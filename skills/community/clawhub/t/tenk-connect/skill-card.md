## Description: <br>
Connect your TenK account to your AI assistant to log practice sessions, check progress, and manage your 10,000-hour journey from chat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OscarCode9](https://clawhub.ai/user/OscarCode9) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and TenK users use this skill to connect an AI assistant to a TenK account, view tracked skills and progress, and record deliberate-practice sessions from chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The current release has an input-handling flaw in its logging flow that could let crafted text run unintended local code. <br>
Mitigation: Prefer a fixed release before installing; if used anyway, install only on a trusted machine, avoid unusual punctuation in skill names or log notes, and verify each session before recording it. <br>
Risk: The skill stores a TenK authentication token locally for API access. <br>
Mitigation: Use it only on a trusted device, keep the token file private, and run logout when finished or when access should be revoked. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/OscarCode9/tenk-connect) <br>
- [TenK app](https://tenk.oventlabs.com) <br>
- [Project homepage](https://github.com/OscarCode9/tenK) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown with shell command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local shell script that calls the TenK API after OAuth device-flow authentication.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
