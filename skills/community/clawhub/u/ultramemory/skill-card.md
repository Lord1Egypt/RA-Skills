## Description: <br>
Ultramemory provides structured AI agent memory with temporal versioning, relational tracking, and semantic search for storing facts, recalling context, searching past conversations, tracking knowledge changes, and building entity profiles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jared-goering](https://clawhub.ai/user/jared-goering) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Ultramemory to add structured long-term memory, semantic and temporal recall, relation tracking, and entity profiles to AI agent workflows across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Long-term conversation facts may be stored, searched later, and resurfaced in future agent contexts. <br>
Mitigation: Avoid storing secrets, credentials, regulated personal data, or private client material unless explicit approval and a deletion process are in place. <br>
Risk: Ingest can send memory content to Anthropic or OpenAI for LLM fact extraction. <br>
Mitigation: Use explicit per-item ingest and review data sensitivity before ingestion. <br>
Risk: Automatic transcript ingest or startup prompt injection can expose or amplify stale or sensitive context. <br>
Mitigation: Prefer explicit recall and ingest workflows, and review recalled context before relying on it. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jared-goering/ultramemory) <br>
- [Ultramemory GitHub repository](https://github.com/jared-goering/ultramemory) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python examples, compact text recall blocks, and JSON CLI responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recall output is compact prompt context; search, graph, stats, history, and profile commands can return JSON.] <br>

## Skill Version(s): <br>
0.2.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
