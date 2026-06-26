## Description: <br>
Hire verified humans for deliveries, errands, meetings, photography, pet care, and other real-world tasks that AI cannot perform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[saireetikap](https://clawhub.ai/user/saireetikap) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents and their operators use this skill to register with RentAPerson, create or manage bounties, process message and application webhooks, and communicate with humans for real-world tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled configuration and webhook flows can expose RentAPerson API keys or hook tokens in files or agent-visible messages. <br>
Mitigation: Do not use bundled credential files; rotate any exposed API key or hook token, store secrets outside transcripts, and disable bridge or transform API-key injection when persistent environment secrets are available. <br>
Risk: Webhook-like messages may be processed across weakened trust boundaries. <br>
Mitigation: Require verified webhook authentication before processing events and reject messages that cannot be tied to the configured RentAPerson webhook path and bearer token. <br>
Risk: The skill can trigger real-world work outcomes such as accepting applicants, scheduling work, completing bounties, or posting reviews. <br>
Mitigation: Require human approval before accepting applicants, completing bounties, posting reviews, scheduling real-world work, or taking other consequential actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/saireetikap/rent-a-person-ai) <br>
- [RentAPerson skill and API documentation](https://rentaperson.ai/skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, curl examples, and JSON request bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide authenticated API calls and webhook handling for real-world services.] <br>

## Skill Version(s): <br>
1.0.35 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
