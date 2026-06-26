## Description: <br>
Session Compact helps OpenClaw agents manage long conversations by compressing prior session history into structured summaries while preserving recent context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdc-creator](https://clawhub.ai/user/sdc-creator) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to reduce token consumption in long-running sessions, inspect compaction status, and configure automatic or manual session compression. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The plugin can expose or alter sensitive conversation data while compacting prior chat history. <br>
Mitigation: Avoid using it with secrets or sensitive business data unless retention controls, storage permissions, and review practices are appropriate for the deployment. <br>
Risk: The implementation processes prior chat history with an LLM. <br>
Mitigation: Use only with conversations that are acceptable for the configured model and provider, and redact sensitive data before compaction where possible. <br>
Risk: Evidence security guidance identifies an unsafe shell-based LLM invocation. <br>
Mitigation: Replace the shell invocation with a scoped API call before using the plugin in higher-trust environments. <br>
Risk: Evidence security guidance identifies plaintext session storage. <br>
Mitigation: Tighten session storage permissions, retention controls, and local access policies before using the plugin with sensitive sessions. <br>


## Reference(s): <br>
- [ClawHub Package Page](https://clawhub.ai/sdc-creator/session-compact-skill) <br>
- [README](artifact/README.md) <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [Troubleshooting](artifact/TROUBLESHOOTING.md) <br>
- [Test Verification Report](artifact/TEST_VERIFICATION_REPORT.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May summarize previous conversation history and session metadata when invoked by an OpenClaw agent.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
