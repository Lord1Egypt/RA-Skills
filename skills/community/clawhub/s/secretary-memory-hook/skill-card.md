## Description: <br>
Automatically records short conversation snippets, creates session summaries before compaction, and reloads prior context after compaction for OpenClaw Secretary Memory workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wgj24](https://clawhub.ai/user/wgj24) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this hook to automate Secretary Memory behavior during conversation compaction. It helps retain session summaries, maintain a local memory index, and reload prior context for later turns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Conversation snippets may be retained in local memory files. <br>
Mitigation: Enable the hook only in workspaces where local memory retention is acceptable, and review retained memory files before using it with sensitive conversations. <br>
Risk: Top-level memory markdown files may be moved automatically before compaction. <br>
Mitigation: Back up the memory directory and review the automatic file movement behavior before enabling the hook in important or regulated workspaces. <br>
Risk: The hook depends on separate secretary-memory Python scripts and shell command execution. <br>
Mitigation: Verify the dependent scripts from a trusted source and review the command construction before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wgj24/secretary-memory-hook) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files, Shell commands, Configuration] <br>
**Output Format:** [Local markdown/log files and context text produced through OpenClaw hook execution] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, Python3, and the separate secretary-memory scripts; preference extraction is documented but currently disabled in the artifact notes.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
