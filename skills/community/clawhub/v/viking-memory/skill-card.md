## Description: <br>
OpenViking long-term memory skill for semantic retrieval of user preferences, conversation history, and important information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[forvendettaw](https://clawhub.ai/user/forvendettaw) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to let an agent search, store, list, and read long-term memories through a local OpenViking memory service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist conversation-derived information without clear consent, retention, or deletion controls. <br>
Mitigation: Configure the agent to ask before saving memories, avoid storing secrets or sensitive personal data, and keep an inspection and deletion process available. <br>
Risk: The skill sends memory operations to a local OpenViking service. <br>
Mitigation: Install only when a trusted local OpenViking memory store is expected and available. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/forvendettaw/viking-memory) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, API calls] <br>
**Output Format:** [Text responses with structured JSON details from local OpenViking API calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local HTTP service at 127.0.0.1:18790 for memory search, storage, listing, reading, and status checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
