## Description: <br>
Social Hub Server is a centralized OpenClaw matching engine that receives user profile summaries from personal agents, maintains a shared registry, evaluates relationship matches, coordinates mutual confirmations, and collects feedback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[FreeAI-io](https://clawhub.ai/user/FreeAI-io) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators running a Social Hub deployment use this skill to operate a central relationship-matching service across multiple users' personal agents. It processes profile updates, performs scheduled and event-driven match scoring, sends filtered match notifications, and records match decisions and feedback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill centralizes sensitive multi-user profile, relationship, disclosure, match-history, and feedback data. <br>
Mitigation: Define explicit user consent, review, deletion, retention, and data-access controls before deployment. <br>
Risk: The skill depends on recurring automation and agent-to-agent group messages for profile updates, match decisions, and notifications. <br>
Mitigation: Restrict group membership, authenticate agent messages, and monitor automated match actions before sending user-facing introductions. <br>
Risk: Operational logs may expose sensitive matching activity or profile-derived information. <br>
Mitigation: Limit log access, avoid recording private profile fields, and set a retention period appropriate for the deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/FreeAI-io/social-hub-server) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, configuration, guidance] <br>
**Output Format:** [Markdown/text guidance with JSON message, registry, and match-history examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational group messages, match notifications, confirmation updates, feedback records, and scheduled task guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
