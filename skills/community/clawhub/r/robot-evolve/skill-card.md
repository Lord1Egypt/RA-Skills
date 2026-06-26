## Description: <br>
Robot Evolve helps an agent run low-risk workspace evolution tasks such as health checks, memory maintenance, temporary-file cleanup, installed-skill scanning, knowledge capture, audit logging, and progress reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pengpengliu1212-art](https://clawhub.ai/user/pengpengliu1212-art) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agent operators and developers use this skill to keep an agent workspace tidy, summarize or retain selected memory/session content, scan installed skill files for basic issues, and produce an evolution report after maintenance activity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify workspace memory and persist selected session-state content locally. <br>
Mitigation: Review and constrain the scripts before use, keep backups of MEMORY.md, and avoid running it in workspaces containing secrets or sensitive session notes. <br>
Risk: The skill can move old temporary files, scan installed skills, and write evolution logs. <br>
Mitigation: Run it only in an intended workspace with reviewed paths and inspect generated logs and moved files after execution. <br>
Risk: The security guidance says --dry-run should not be treated as a safe preview. <br>
Mitigation: Use an isolated test workspace for validation before running the skill on important local data. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/pengpengliu1212-art/robot-evolve) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, command-line text, JSON configuration, and local Markdown log or knowledge files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local audit/evolution logs, memory summaries, knowledge files, and move old temporary files into a workspace trash directory.] <br>

## Skill Version(s): <br>
3.0.8 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
