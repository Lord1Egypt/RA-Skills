## Description: <br>
Turn every Claude Code session into an Obsidian note by generating structured Markdown reports and interactive Canvas visual maps with automatic project detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ChatRichAi](https://clawhub.ai/user/ChatRichAi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers using Claude Code use this skill to save session plans and implementation reports into an Obsidian vault as Markdown notes and Canvas maps. It is intended for local documentation of project work, design decisions, file changes, and follow-up tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Plans, file paths, design decisions, and session summaries may be saved into the configured Obsidian vault. <br>
Mitigation: Review notes before syncing sensitive work and avoid including secrets or confidential material. <br>
Risk: Optional auto-sync configuration can cause future sessions to sync plans or reports automatically. <br>
Mitigation: Enable CLAUDE.md auto-sync only when persistent session documentation is desired. <br>
Risk: Incorrect vault configuration can write files to an unintended local directory. <br>
Mitigation: Confirm the OBSIDIAN_VAULT path before first use and review the reported output paths after each sync. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ChatRichAi/sync-obsidian) <br>
- [Publisher profile](https://clawhub.ai/user/ChatRichAi) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown notes plus Obsidian Canvas JSON files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local files to a user-configured Obsidian vault and reports the generated Markdown and Canvas paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
