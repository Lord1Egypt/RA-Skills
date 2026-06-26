## Description: <br>
Scan openclaw.json for plaintext secrets (tokens, API keys, passwords) and migrate them to environment variables using SecretRef. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maoisdamao](https://clawhub.ai/user/maoisdamao) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to audit local OpenClaw configuration for plaintext credentials and migrate confirmed findings to SecretRef-backed environment variables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local OpenClaw configuration and can edit openclaw.json and the user's shell profile during migration. <br>
Mitigation: Review scan findings and dry-run output, confirm the profile path, and require explicit user confirmation before applying changes. <br>
Risk: Environment-variable migration moves secrets out of openclaw.json but can still leave them as plaintext in shell profile files. <br>
Mitigation: For higher-security environments, prefer file- or exec-based SecretRef and restrict permissions on any secret files. <br>
Risk: The automatic backup file can retain plaintext credentials after migration. <br>
Mitigation: Protect the .bak file while rollback is needed, then remove it or use the cleanup path after verification. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/maoisdamao/token-safety-checker) <br>
- [Project homepage](https://github.com/maoisdamao/token-safety-checker) <br>
- [Publisher profile](https://clawhub.ai/user/maoisdamao) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON snippets and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scan output reports field paths, suggested environment variable names, lengths, and risk levels without printing secret values.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
