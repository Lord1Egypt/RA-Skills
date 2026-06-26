## Description: <br>
Automatic cloud backup and sync for OpenClaw memory files, with S3-compatible storage backup, restore, retention, and a local dashboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neroagent](https://clawhub.ai/user/neroagent) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to back up, inspect, and restore local memory files through S3-compatible cloud storage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill backs up broad memory data that may contain secrets or regulated information. <br>
Mitigation: Use a dedicated least-privilege bucket and prefix, avoid backing up sensitive data, and review the memory directory before enabling sync. <br>
Risk: The server security summary says the artifact claims encryption, but the reviewed code does not implement client-side encryption. <br>
Mitigation: Treat uploaded backups as plaintext unless real client-side encryption is added and verified. <br>
Risk: Restore can overwrite local memory state. <br>
Mitigation: Create a separate local copy of the memory directory before testing or running restore. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/neroagent/session-sync-cloud) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, files, configuration, shell commands, guidance] <br>
**Output Format:** [JSON responses, generated local files, configuration snippets, and Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Status and restore outputs are returned as JSON; backup activity can write manifests, logs, restored memory files, and a local dashboard file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
