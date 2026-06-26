## Description: <br>
Task manager for AI agents. Works instantly - no account, no phone needed. 19 tools for nested task trees, batch ops, local storage, optional phone sync. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[banonanon](https://clawhub.ai/user/banonanon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use SHrimp Tasks to let agents create, search, update, batch, sync, and manage nested task trees with local storage and optional iOS pairing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paired mode can let agents access or change prompt sections, provider settings, inbox items, and activity logs. <br>
Mitigation: Confirm the paired-mode data and setting boundaries before use, and require explicit approval for prompt changes, provider-setting changes, permanent deletes, and batch operations. <br>
Risk: Installation runs a pinned external npm MCP package. <br>
Mitigation: Install only when the external package source and pinned version are acceptable for the environment. <br>


## Reference(s): <br>
- [SHrimp homepage](https://hermitshell.ai) <br>
- [ClawHub skill page](https://clawhub.ai/banonanon/shrimp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and MCP tool guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can expose task data, prompt sections, provider settings, inbox items, and activity logs when paired with the iOS app.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
