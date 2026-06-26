## Description: <br>
Thought-Retriever extracts reusable, high-confidence insights from conversation answers and stores them as ontology-backed Thought memories for later retrieval and memory evolution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[as1113435](https://clawhub.ai/user/as1113435) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators can use this skill as a post-turn memory workflow that extracts candidate insights, filters low-confidence entries, deduplicates similar Thoughts, and updates an ontology-backed memory store. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Conversation content and stored memory content may be sent to the declared external LLM provider. <br>
Mitigation: Use only after confirming the provider is acceptable for the data being processed, and redact or avoid sensitive conversation content before use. <br>
Risk: The artifact contains an embedded API key. <br>
Mitigation: Replace or remove the embedded key before installation and use a secret-management mechanism controlled by the deployment environment. <br>
Risk: Long-term memories are stored locally without clear user controls for review, deletion, or disabling capture. <br>
Mitigation: Add explicit opt-in for post-turn capture and provide controls to inspect, delete, disable, or redact stored memories. <br>


## Reference(s): <br>
- [Thought-Retriever on ClawHub](https://clawhub.ai/as1113435/thought-retriever) <br>
- [arXiv:2604.12231](https://arxiv.org/abs/2604.12231) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, Python code behavior, CLI output, and JSON-like status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates local ontology memory records and reports counts for retrieved, candidate, and newly added Thoughts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
