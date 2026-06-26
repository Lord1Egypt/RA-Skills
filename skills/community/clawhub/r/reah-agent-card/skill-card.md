## Description: <br>
Retrieve masked card info from Reah using an access key; handles session generation, secure fetch, and decryption for agents automatically. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[axelzou](https://clawhub.ai/user/axelzou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve masked Reah card details from agents.reah.com after providing an access key or explicitly confirming a current environment-key read. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent may gain access to Reah payment-card details. <br>
Mitigation: Install only for intentional Reah card workflows, use limited or virtual cards, and require explicit approval for every key read and purchase detail. <br>
Risk: Sensitive access keys, session secrets, or card details could be exposed in user-facing output. <br>
Mitigation: Do not display full access keys or raw secret keys; mask card info part A and redact card info part B. <br>
Risk: Broad payment-card use without transaction-level controls can create financial misuse risk. <br>
Mitigation: Rotate access keys periodically and require user approval for purchase details before any transaction-oriented workflow proceeds. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/axelzou/reah-agent-card) <br>
- [Publisher Profile](https://clawhub.ai/user/axelzou) <br>
- [Reah GraphQL Endpoint](https://agents.reah.com/graphql) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node or curl; environment-based key reads require REAH_AGENT_KEYS and explicit manual confirmation for each read.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
