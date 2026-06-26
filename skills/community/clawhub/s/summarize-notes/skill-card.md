## Description: <br>
每日笔记深度解读。从笔记目录筛选当日笔记，分类、逐条提炼要点，最后做深度关联分析和洞察挖掘。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YoungAndSure](https://clawhub.ai/user/YoungAndSure) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to summarize daily Markdown or text notes from a configured notes directory, categorize them, extract per-note summaries, and produce deeper cross-note and historical analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads today's notes and searches older notes in the configured folder, which can include sensitive personal or private material. <br>
Mitigation: Set NOTES_DIR to a narrow notes-only directory, exclude sensitive journals or private archives, and confirm before historical analysis. <br>
Risk: Full-text model analysis of current and historical notes may expose more content than needed for the requested summary. <br>
Mitigation: Use snippets or truncated note text when possible, and ask for confirmation before sending full notes into analysis. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/YoungAndSure/summarize-notes) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with tables, summaries, analysis sections, and inline shell commands for note discovery.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured NOTES_DIR or a user-provided notes directory; supports Markdown and text notes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
