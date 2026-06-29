## Description: <br>
Generate synthetic test data for persons, companies, families, e-commerce, auth systems, CRM, financial records, technical IDs, edge cases, and deterministic seeded datasets through AgentPMT-hosted remote tool calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and QA engineers use this skill to generate fake customer, business, financial, technical, and relational datasets for testing, demos, validation, and stress testing without relying on real user data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill invokes a remote paid AgentPMT synthetic-data service, so accidental or repeated calls may consume credits. <br>
Mitigation: Invoke it deliberately, monitor credit use, and use small seeded requests when validating workflows. <br>
Risk: Generated values can include credit-card-like, token-like, or injection-pattern strings intended for testing. <br>
Mitigation: Keep generated outputs in isolated development or testing workflows and avoid mixing them with production secrets, payment data, or customer records. <br>
Risk: Remote tool inputs may expose unnecessary private context if prompts include unrelated sensitive data. <br>
Mitigation: Send only the minimum parameters needed for synthetic data generation and avoid including private user, account, wallet, or credential material. <br>


## Reference(s): <br>
- [Synthetic Data Generator on ClawHub](https://clawhub.ai/agentpmt/synthetic-data-generator) <br>
- [AgentPMT Marketplace Page](https://www.agentpmt.com/marketplace/synthetic-data-generator) <br>
- [Action Schema Reference](artifact/schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON request examples and generated JSON data from remote tool calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports deterministic seeding, locale-aware data, edge-case generation, and small to large dataset sizes through the AgentPMT tool schema.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
