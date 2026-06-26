## Description: <br>
Persistent memory engine for AI agents with semantic recall, hotness prioritization, importance weighting, time decay, and auto-compaction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chen-feng123](https://clawhub.ai/user/chen-feng123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add a local, zero-dependency memory store that can write, search, retrieve, compact, and clean up agent memories. It is suited to agents that need persistent recall from a local JSON file without a network service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores user-added memories in a local plaintext JSON file, which can expose sensitive information if secrets or private data are saved. <br>
Mitigation: Do not store API keys, passwords, private customer data, or other sensitive records; restrict file access to the workspace where the memory store is used. <br>
Risk: Cleanup, clear, and compact operations can change or remove stored memories. <br>
Mitigation: Back up MEMORY_STORE.json before running destructive or compaction operations when the memory contents matter. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/chen-feng123/quickrecall) <br>
- [Memory Enhancement Engine API Specification](references/API_SPEC.md) <br>
- [Memory Enhancement Engine Usage Guide](references/USE_GUIDE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript examples, shell commands, and JSON-like memory records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists user-added memory content to a local JSON store and returns scored recall results.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
