## Description: <br>
Safely create and manage subagents through a strict wrapper instead of calling sessions_spawn directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devymex](https://clawhub.ai/user/devymex) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to standardize subagent delegation, generate safe spawn payloads, and preserve multi-round subagent context in auditable Markdown files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent full-text context files may retain sensitive task background, external messages, and child outputs. <br>
Mitigation: Avoid using the skill with secrets, credentials, regulated data, or sensitive personal data unless a separate redaction and retention process is in place. <br>
Risk: Multi-round delegation reuses previous context, so later subagents may see earlier task history. <br>
Mitigation: Create a new context file for unrelated work or whenever prior context should not be shared. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/devymex/safe-subagent-spawn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell commands and generated JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates persistent full-text context files and ready-to-use subagent spawn payloads.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
