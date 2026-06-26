## Description: <br>
Sophie Mem0 provides persistent semantic memory for an OpenClaw agent, including memory storage, retrieval, deletion, health checks, and automatic extraction of important user details from conversation text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingdangmaoup](https://clawhub.ai/user/dingdangmaoup) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add long-term semantic memory to an OpenClaw agent backed by mem0 and a vector database. It is intended for storing, searching, listing, and deleting user memories across sessions, with optional automatic extraction from chat text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic mode can store personal conversation details without a separate manual confirmation step. <br>
Mitigation: Use automatic extraction only in contexts where users expect long-term memory, and disable it for sensitive conversations. <br>
Risk: Memory content may be processed by the configured LLM and embedding providers. <br>
Mitigation: Review provider configuration before use and avoid sending secrets, regulated data, or other sensitive personal information to external services. <br>
Risk: Persistent memory in Qdrant and the local configuration file can expose private information or API credentials if not protected. <br>
Mitigation: Restrict access to the configuration file and vector database, and verify list and delete workflows before relying on stored memories. <br>


## Reference(s): <br>
- [Sophie Mem0 ClawHub listing](https://clawhub.ai/dingdangmaoup/sophie-mem0) <br>
- [Publisher profile](https://clawhub.ai/user/dingdangmaoup) <br>
- [artifact/SKILL.md](artifact/SKILL.md) <br>
- [artifact/scripts/auto_memory.py](artifact/scripts/auto_memory.py) <br>
- [artifact/scripts/mem0_cli.py](artifact/scripts/mem0_cli.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, and command-line text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read or write persistent memories through the configured mem0 provider and vector database.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
