## Description: <br>
Automates session wrap-up by preserving session context, updating memory and PARA notes, and optionally committing and pushing repository changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neroagent](https://clawhub.ai/user/neroagent) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to close a work session by recording summaries, carrying forward long-term memory, updating open loops, and coordinating repository wrap-up steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically stage, commit, and push repository changes, which may include unrelated work or sensitive files. <br>
Mitigation: Review carefully before installing; use only in repositories prepared for automatic wrap-up, or change git operations to stage explicit wrap-up files and require confirmation before pushing. <br>
Risk: Release security evidence reports a command-injection issue in the commit flow. <br>
Mitigation: Do not pass untrusted commit messages, and fix the command execution path to avoid shell interpretation before using the git commit automation. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/neroagent/session-wrap-up-premium) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands, Configuration] <br>
**Output Format:** [Markdown reports, JSON summaries, and workspace file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can update memory and notes files and run git add, commit, and push operations when invoked.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
