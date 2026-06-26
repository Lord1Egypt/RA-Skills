## Description: <br>
Praesidia helps OpenClaw assistants verify AI agents, check trust scores, fetch A2A agent cards, discover marketplace agents, and apply guardrails for security and compliance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[msoica](https://clawhub.ai/user/msoica) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and AI assistant operators use this skill to check agent identity and trust, discover suitable agents, and manage Praesidia guardrails for security, moderation, and compliance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide live guardrail changes for agents. <br>
Mitigation: Require the assistant to show the proposed guardrail change and obtain explicit confirmation before making POST requests; test changes in staging when possible. <br>
Risk: Praesidia API credentials or endpoints could be misconfigured. <br>
Mitigation: Use a least-privilege API key and keep PRAESIDIA_API_URL pointed at a trusted endpoint. <br>
Risk: Content validation may send confidential or regulated content to Praesidia. <br>
Mitigation: Avoid validating sensitive content unless Praesidia's data handling is acceptable for the user's environment. <br>


## Reference(s): <br>
- [Praesidia](https://praesidia.ai) <br>
- [Praesidia API documentation](https://app.praesidia.ai/docs/api) <br>
- [A2A protocol](https://a2a-protocol.org) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, configuration] <br>
**Output Format:** [Markdown guidance with JSON and JavaScript request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PRAESIDIA_API_KEY for authenticated Praesidia operations.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
