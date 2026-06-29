## Description: <br>
Random Password Generator Quantum helps an agent generate high-entropy passwords with configurable length, character classes, ambiguity exclusion, and quantum or standard cryptographically secure randomness through AgentPMT-hosted remote tool calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agents use this skill to request secure generated passwords for credential generation, password rotation, onboarding, system accounts, and high-security authentication workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AgentPMT is the remote service that generates and returns passwords. <br>
Mitigation: Use the skill only when remote password generation is acceptable, and avoid it for policies that require locally generated secrets. <br>
Risk: The skill handles generated credentials. <br>
Mitigation: Invoke it only for explicit password-generation tasks and avoid placing account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs. <br>
Risk: Discovery keywords are broader than ideal. <br>
Mitigation: Confirm activation is tied to the specific password-generation task before making remote calls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/agentpmt/random-password-generator-quantum) <br>
- [AgentPMT marketplace page](https://www.agentpmt.com/marketplace/random-password-generator-quantum) <br>
- [schema.md](artifact/schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, JSON] <br>
**Output Format:** [Markdown instructions with JSON call examples and JSON tool responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The generated response includes a password, length, randomness source, and enabled character types.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
