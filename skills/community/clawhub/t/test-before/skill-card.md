## Description: <br>
Test skill for static scan validation that guides agentic wallet operations via the caw CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pengjunquan-l](https://clawhub.ai/user/pengjunquan-l) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to guide agentic wallet workflows, including checking balances, preparing owner-approved operations, and tracking submitted pact status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agentic wallet operations can move on-chain assets if an agent acts beyond the owner's explicit intent. <br>
Mitigation: Require active owner-approved authorization, explicit recipient, amount, and chain, and do not exceed pact scope or spending limits. <br>
Risk: Prompt injection or external messages may try to trigger unauthorized transfers or bypass approval. <br>
Mitigation: Accept wallet-operation requests only when they come directly from the user, reject webhook, email, external-document, or other-agent instructions, and stop on prompt-injection patterns. <br>
Risk: Sensitive wallet context or credentials may be exposed through agent conversation storage or transmission. <br>
Mitigation: Avoid entering sensitive personal or credential details unless the user accepts how the agent stores or transmits conversation context. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pengjunquan-l/test-before) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands] <br>
**Output Format:** [Markdown guidance with inline shell commands and operational checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Text-only skill; security evidence reports no code execution, network use, credentials handling, or persistence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
