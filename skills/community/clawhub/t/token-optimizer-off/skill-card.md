## Description: <br>
Token Optimizer Off compresses long OpenClaw agent conversation histories into concise summaries and task-scoped memory to reduce context usage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thanksandyou](https://clawhub.ai/user/thanksandyou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to monitor long OpenClaw sessions, compress session history, and load only relevant memory for the current task. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send conversation content to an AI provider for compression. <br>
Mitigation: Prefer dry-run or manual compression first, and review summaries for secrets before storing or reusing them. <br>
Risk: The skill stores compressed memory across sessions in the global OpenClaw memory directory. <br>
Mitigation: Review generated memory files periodically and limit retained content to information that should persist across sessions. <br>
Risk: The uninstall guidance can delete all OpenClaw memory if run as written. <br>
Mitigation: Back up or inspect the OpenClaw memory directory before deleting it, and only remove it when full memory erasure is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thanksandyou/token-optimizer-off) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact installation guide](artifact/INSTALL.md) <br>
- [Artifact changelog](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and command-line text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write compressed session summaries and state files under the OpenClaw memory directory when run outside dry-run mode.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
