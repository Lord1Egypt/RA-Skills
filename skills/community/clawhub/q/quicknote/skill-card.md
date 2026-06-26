## Description: <br>
Lightning-fast note-taking tool. Capture thoughts instantly, pin important notes, search across all entries, and export to markdown. Zero config, local storage, instant access. Perfect for quick ideas, reminders, and knowledge snippets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers can use Quicknote to capture, search, review, and export local notes from the terminal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Notes are stored locally in plaintext under ~/.local/share/quicknote. <br>
Mitigation: Avoid storing passwords, tokens, or confidential material, and apply appropriate local file permissions. <br>
Risk: Exported note files may be easier to sync, share, or leave behind. <br>
Mitigation: Review generated exports before sharing and remove stale exports when they are no longer needed. <br>
Risk: The documented command set and implemented script commands do not fully match. <br>
Mitigation: Verify available commands with the installed help output before relying on a workflow. <br>


## Reference(s): <br>
- [Quicknote on ClawHub](https://clawhub.ai/ckchzh/quicknote) <br>
- [BytesAgain Feedback](https://bytesagain.com/feedback) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files] <br>
**Output Format:** [Terminal text plus local export files in markdown, JSON, CSV, or TXT formats] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores notes locally in plaintext under ~/.local/share/quicknote.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata; artifact frontmatter and script declare 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
