## Description: <br>
Cloud-native persistent memory for OpenClaw agents that auto-captures conversation facts, auto-recalls relevant context before replies, and supports hybrid search, query rewrite, and experience learning behind one API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[frf12](https://clawhub.ai/user/frf12) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to give OpenClaw agents persistent, cross-session memory for preferences, decisions, facts, and reusable tool-use experiences. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic memory capture can retain conversation-derived facts in a third-party cloud memory system across sessions and devices. <br>
Mitigation: Use only for data approved for third-party retention, avoid secrets and regulated data, and confirm users can view, correct, and delete stored memories. <br>
Risk: Auto-recalled memories can place stale, incorrect, or overly broad personal context into future prompts. <br>
Mitigation: Limit autoRecall and recallLimit where appropriate, review recalled context during sensitive work, and use memory_forget for outdated or incorrect records. <br>
Risk: The m0 plugin requires an API key and endpoint configuration for the memory service. <br>
Mitigation: Use a dedicated API key, keep endpoint and key configuration scoped to the intended service, and rotate credentials if exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/frf12/seekdb-memory) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes memory tool usage examples for recall, storage, deletion, and experience lookup.] <br>

## Skill Version(s): <br>
0.2.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
