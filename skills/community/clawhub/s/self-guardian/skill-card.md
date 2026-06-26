## Description: <br>
Lightweight self-monitoring and self-constraining rules to prevent accidental file deletions, dangerous commands, and risky operations. Activates automatically on file/shell operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vaderyang](https://clawhub.ai/user/vaderyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to make coding agents pause, explain, and request confirmation before destructive file operations, risky shell commands, broad refactors, dependency changes, or database operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can over-trigger confirmation prompts during normal refactors, cleanup work, or routine shell usage. <br>
Mitigation: Use it when extra caution is desired and treat additional prompts as review points before continuing. <br>
Risk: Recovery breadcrumbs that read existing files into chat history could expose secrets, keys, databases, or private files if used carelessly. <br>
Mitigation: Do not copy sensitive files into chat history; use local backups, git checkpoints, or other private recovery mechanisms for sensitive material. <br>


## Reference(s): <br>
- [Self-Guardian on ClawHub](https://clawhub.ai/vaderyang/self-guardian) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with clarification prompts, brief explanations, confirmations, and inline shell command handling.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Adds caution prompts before risky file, dependency, database, or shell operations and may increase confirmation frequency during normal edits.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
