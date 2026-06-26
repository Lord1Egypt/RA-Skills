## Description: <br>
Searches local files and indexed content on macOS using Spotlight and mdfind. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[li-hongmin](https://clawhub.ai/user/li-hongmin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to find local macOS files, documents, and indexed content in user-specified directories before asking for confirmation to open or summarize results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local Spotlight search results can reveal sensitive file paths or document names. <br>
Mitigation: Keep searches scoped to user-specified directories and treat returned paths as potentially sensitive. <br>
Risk: Opening or summarizing discovered files may expose private content beyond the user's original search request. <br>
Mitigation: Present search results first and require explicit user approval before reading any found file. <br>
Risk: Administrative Spotlight indexing commands can change system settings. <br>
Mitigation: Do not run sudo commands from the skill; show such commands only as information for the user to run directly. <br>


## Reference(s): <br>
- [ClawHub Spotlight release page](https://clawhub.ai/li-hongmin/spotlight) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [spotlight-search.sh](artifact/scripts/spotlight-search.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text search results and Markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires macOS Spotlight indexing; searches are scoped by directory and optional result limit.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
