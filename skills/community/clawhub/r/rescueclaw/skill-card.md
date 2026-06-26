## Description: <br>
Provides a checkpoint API and CLI workflow for backing up local OpenClaw state before risky operations and clearing checkpoints after success. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harman314](https://clawhub.ai/user/harman314) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use RescueClaw to create and clear local checkpoints around risky configuration changes, skill installs, or gateway updates so local recovery is possible if an operation fails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer downloads and installs a remote executable daemon without published integrity verification in the provided evidence. <br>
Mitigation: Install only after reviewing the publisher and release pipeline, and prefer releases with checksums, signatures, or manual verification steps. <br>
Risk: Checkpoint documentation may imply stronger rollback protection than the helper code can verify on its own. <br>
Mitigation: Confirm the daemon is running and has acknowledged checkpoint requests before relying on rollback behavior for risky operations. <br>


## Reference(s): <br>
- [RescueClaw ClawHub listing](https://clawhub.ai/harman314/rescueclaw) <br>
- [RescueClaw GitHub Releases](https://github.com/harman314/rescueclaw/releases) <br>
- [Publisher profile](https://clawhub.ai/user/harman314) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JavaScript snippets and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes checkpoint, clear, status, and daemon installation guidance for user-local paths.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
