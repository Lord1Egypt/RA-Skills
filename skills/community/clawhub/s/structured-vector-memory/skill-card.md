## Description: <br>
Structured Vector Memory helps OpenClaw users manage layered agent memory with LanceDB Pro, scheduled daily summaries, weekly distillation, deduplication, scoped recall, and archiving. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kylin19860916](https://clawhub.ai/user/kylin19860916) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to set up and operate a structured memory workflow that captures important decisions, writes daily summaries, distills long-term memory, and separates memories by scope. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can repeatedly review conversations and change persistent agent memory without clear per-action approval. <br>
Mitigation: Enable cron and autoCapture/autoRecall only after reviewing which sessions may be summarized, and require manual review for changes to MEMORY.md, SYSTEM_GUIDE.md, archived memories, or vector-memory deletions. <br>
Risk: The workflow depends on memory-lancedb-pro and Jina for conversation-derived memory storage and retrieval. <br>
Mitigation: Audit the separate plugin and Jina data handling before deployment, and avoid storing sensitive sessions unless the environment permits it. <br>


## Reference(s): <br>
- [AGENTS.md memory rules template](references/agents-rules.md) <br>
- [ClawHub skill page](https://clawhub.ai/kylin19860916/structured-vector-memory) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces scheduled memory-maintenance instructions, HEARTBEAT task prompts, and human-readable memory summaries.] <br>

## Skill Version(s): <br>
3.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
