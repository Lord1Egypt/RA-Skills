## Description: <br>
Write session summaries to daily memory files and search session history so OpenClaw can recall and cite past conversations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[breezezephyr](https://clawhub.ai/user/breezezephyr) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw users and agents use this skill to turn local session logs for a date into workspace memory and to search prior conversations by keyword or date range. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose or retain sensitive content from local OpenClaw session logs by writing excerpts into workspace memory files. <br>
Mitigation: Run it only for intended dates or queries, avoid sessions containing secrets or confidential data, and review or delete generated memory files when they should not be retained. <br>
Risk: Search results and generated memory summaries may include partial conversation snippets without full context. <br>
Mitigation: Review the source session snippets before relying on them for important decisions or future memory recall. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/breezezephyr/session-memory-workspace) <br>
- [Publisher profile](https://clawhub.ai/user/breezezephyr) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; scripts produce JSON search results and Markdown memory files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js; reads local OpenClaw session JSONL files and can create or append memory/YYYY-MM-DD.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, SKILL.md frontmatter, README.md, _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
