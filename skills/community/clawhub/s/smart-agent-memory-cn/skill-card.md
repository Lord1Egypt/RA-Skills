## Description: <br>
Provides a cross-platform long-term memory system for OpenClaw agents with layered context retrieval, skill experience memory, structured Markdown/JSON/SQLite storage, search, archiving, and reflection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TNTest](https://clawhub.ai/user/TNTest) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to give OpenClaw agents persistent local memory, scoped context recall, and reusable lessons across sessions without installing external dependencies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores broad conversation data as shared long-term local memory. <br>
Mitigation: Set rules that prohibit storing credentials, secrets, regulated data, and sensitive personal details; review exports and session summaries before use. <br>
Risk: The skill can generate new agent skills in the live skills directory. <br>
Mitigation: Manually inspect any generated SKILL.md and scan extracted skills before allowing agents to use them. <br>
Risk: Scheduled memory workflows can retain or summarize data in the background. <br>
Mitigation: Avoid scheduled backfill, reflection, or garbage-collection jobs unless background retention is intended and reviewed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/TNTest/smart-agent-memory-cn) <br>
- [Publisher profile](https://clawhub.ai/user/TNTest) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Configuration] <br>
**Output Format:** [Plain text and Markdown from CLI commands, with JSON exports, configuration snippets, and generated SKILL.md files when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local memory files under ~/.openclaw/workspace/memory and can create extracted skills under ~/.openclaw/skills.] <br>

## Skill Version(s): <br>
2.1.1 (source: server release metadata; artifact frontmatter lists 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
