## Description: <br>
Rookie Memory provides a three-tier memory system for AI agents with startup bootstrap, autosave, hybrid retrieval, health analysis, and cleanup commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Rrrker](https://clawhub.ai/user/Rrrker) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Rookie Memory to persist, retrieve, summarize, and clean up conversation memory for AI agents across short-, medium-, and long-term storage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remembered conversation text may be saved locally and sent to the configured BigModel/Zhipu embedding service. <br>
Mitigation: Use a dedicated low-scope API key, avoid storing secrets or regulated data, and install only if the publisher and external embedding service are trusted. <br>
Risk: Long-lived memory records may accumulate stale, sensitive, or unwanted conversation context. <br>
Mitigation: Review the memory directory regularly and use cleanup dry-run mode before deleting records. <br>


## Reference(s): <br>
- [Memory Manager Command Reference](references/references.md) <br>
- [BigModel embedding API endpoint](https://open.bigmodel.cn/api/paas/v4) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance, shell command output, JSON memory records, YAML configuration, and plain-text logs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can persist conversation text locally and in a vector store; embedding calls may send remembered text to the configured BigModel/Zhipu service.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
