## Description: <br>
Fast note-taking and snippet storage for short text snippets, tags, search, and recent-note lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yushimohuang](https://clawhub.ai/user/yushimohuang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and other agent users use this skill to save, list, search, tag, and delete short local notes or snippets during workspace tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Notes are stored as plaintext workspace files and may expose secrets or confidential information if misused. <br>
Mitigation: Use this only for ordinary local notes and snippets; do not save API keys, passwords, tokens, or confidential information. <br>
Risk: Deleting by note ID can remove stored note content. <br>
Mitigation: Confirm the exact note ID before deleting; the Bash script creates a quick-notes.md.bak backup during deletion. <br>
Risk: The skill text includes a PowerShell command, but this artifact only includes the Bash note script. <br>
Mitigation: Use the included Bash script, or run PowerShell only after confirming the referenced script is present and reviewed. <br>


## Reference(s): <br>
- [ClawHub quick-note-tool release page](https://clawhub.ai/yushimohuang/quick-note-tool) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands] <br>
**Output Format:** [Markdown notes stored in a workspace file with plain terminal status text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores notes as plaintext in notes/quick-notes.md and creates a backup when deleting notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
