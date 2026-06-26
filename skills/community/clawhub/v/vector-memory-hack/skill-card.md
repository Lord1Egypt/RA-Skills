## Description: <br>
Fast semantic search for AI agent memory files using TF-IDF and SQLite, enabling local context retrieval from MEMORY.md or markdown documentation without external dependencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mig6671](https://clawhub.ai/user/mig6671) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and AI agent operators use this skill to index local memory or markdown documentation and retrieve relevant sections before a task, reducing the need to read entire memory files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill indexes local memory content into SQLite and can surface sensitive context if credentials or secrets are present in memory files. <br>
Mitigation: Avoid storing credentials in MEMORY.md, review search results before using them, and delete or rebuild the index after removing sensitive entries. <br>
Risk: The skill encourages broad memory search before tasks, which may expose more saved context than the current task requires. <br>
Mitigation: Use targeted queries only when saved context is needed for the current task and keep result counts narrow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mig6671/vector-memory-hack) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash and Python snippets; CLI output as plain text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search output returns top-k scored sections from a local SQLite index.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
