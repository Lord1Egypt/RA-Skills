## Description: <br>
Captures learnings, errors, and corrections to enable continuous improvement for coding agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhihongyee](https://clawhub.ai/user/zhihongyee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to capture corrections, command failures, feature requests, and recurring lessons in local markdown files so future agent work can reuse the learning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may preserve sensitive conversation details, command errors, or project context in durable local markdown files. <br>
Mitigation: Set a clear retention policy for .learnings, redact secrets and personal or customer data before writing entries, and decide whether the directory should be gitignored. <br>
Risk: Promoted learning entries can spread incorrect or over-specific guidance into persistent project instructions. <br>
Mitigation: Require human review before promoting entries to project memory files and keep promoted rules concise, general, and source-aware. <br>
Risk: Optional hook integrations can run automatically during agent workflows. <br>
Mitigation: Enable hooks only after inspecting the referenced scripts and confirming they create sanitized summaries appropriate for the workspace. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zhihongyee/self-improvement-2) <br>
- [Agent Skills specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local learning, error, and feature-request records for later review or promotion.] <br>

## Skill Version(s): <br>
0.1.0 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
