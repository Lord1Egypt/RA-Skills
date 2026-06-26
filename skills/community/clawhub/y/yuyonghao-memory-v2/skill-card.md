## Description: <br>
Memory V2 provides a Chinese-optimized long-term memory system with vector search, knowledge graph linking, entity extraction, and automated memory maintenance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers integrating OpenClaw or similar agent systems use this skill to store, search, link, and maintain long-term conversational or document memories. It is especially suited for Chinese-language memory retrieval with entity extraction and graph relationships. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private or sensitive memories may be persisted in vector and graph stores. <br>
Mitigation: Use an isolated database path, avoid storing raw transcripts by default, add redaction and retention rules, and keep backups before enabling automatic maintenance. <br>
Risk: Optional LLM summarization can send memory content to a configured provider. <br>
Mitigation: Disable or tightly control summarization unless the provider is trusted for the data being processed. <br>
Risk: Automatic maintenance can transform and archive low-priority memories. <br>
Mitigation: Define retention policies, test thresholds on representative data, and back up memory stores before scheduled maintenance. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yuyonghao-123/yuyonghao-memory-v2) <br>
- [Memory V2 skill documentation](artifact/SKILL.md) <br>
- [Memory V2 integration guide](artifact/INTEGRATION.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Code, Configuration] <br>
**Output Format:** [JavaScript module APIs returning JSON-like memory records, search results, entity links, maintenance statistics, and Markdown usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses persistent LanceDB vector storage and JSONL graph storage; first run may download embedding and NER models.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata, artifact SKILL.md, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
