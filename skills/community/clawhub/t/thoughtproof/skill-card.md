## Description: <br>
Epistemic verification for AI agent outputs. Use ThoughtProof to verify AI reasoning, detect blind spots, and build consensus across multiple model families. Triggers: when an agent needs a second opinion, audit trail for decisions, or epistemic consensus. Works with any LLM backend (BYOK). Commands: tp verify, tp deep, tp list, tp show. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ThoughtProof](https://clawhub.ai/user/ThoughtProof) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, engineers, and governance reviewers use ThoughtProof to request multi-model verification of AI reasoning, decisions, and high-stakes questions. It is intended for second opinions, blind spot detection, consensus building, and local audit history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on an external CLI package, provider API keys, third-party model calls, and local history storage. <br>
Mitigation: Review and pin a trusted pot-cli version, use dedicated or restricted provider API keys, monitor billing, and avoid submitting secrets or regulated data unless every configured provider is approved for that use. <br>
Risk: Local verification history may contain sensitive prompts, decisions, or model outputs. <br>
Mitigation: Periodically delete local verification history when it may contain sensitive material. <br>


## Reference(s): <br>
- [ThoughtProof skill page](https://clawhub.ai/ThoughtProof/thoughtproof) <br>
- [ThoughtProof website](https://thoughtproof.ai) <br>
- [Epistemic Block Format](references/block-format.md) <br>
- [Consensus Protocol](references/consensus-protocol.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The wrapper delegates to pot-cli and stores verification blocks locally as JSON history.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
