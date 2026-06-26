## Description: <br>
Safely write or append text content to files only in /home/alfred/.openclaw/workspace/scratch, creating backups before overwrites and rejecting unsafe paths, binary content, and non-text extensions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Nagilem](https://clawhub.ai/user/Nagilem) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to have an agent create, append, or overwrite text files inside a scratch workspace while applying path validation, backup, and confirmation steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary rates the skill suspicious because it asks the agent to use shell commands for file operations more broadly than the safe-file-writing promise. <br>
Mitigation: Install only when scratch-directory file writes are acceptable, review confirmations carefully, and approve shell fallback commands only after checking the exact path and content. <br>
Risk: The skill can create, overwrite, append, and back up text files in the scratch directory. <br>
Mitigation: Use explicit relative paths, reject absolute paths or parent-directory escapes, and keep overwrite confirmations and backups in place. <br>


## Reference(s): <br>
- [Safety Reference](references/safety.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/Nagilem/scratch-file-writer) <br>
- [Publisher Profile](https://clawhub.ai/user/Nagilem) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with file paths, confirmations, and optional shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent instructions for text file creation, appends, overwrites, backups, and error handling within a scratch directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
