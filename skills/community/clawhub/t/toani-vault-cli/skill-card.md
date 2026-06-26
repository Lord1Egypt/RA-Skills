## Description: <br>
Install, configure, and securely operate the Toani Vault CLI for login, health checks, credential metadata reads, and sandbox browser sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[toani](https://clawhub.ai/user/toani) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to install and verify the Toani Vault CLI, authenticate safely, inspect credential metadata, and run remote sandbox browser sessions while keeping token handling explicit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill supports workflows involving bearer tokens and credential-backed CLI operations. <br>
Mitigation: Use placeholder values in examples, avoid logging or committing real tokens, and verify target URLs before credential-backed actions. <br>
Risk: Remote sandbox browser sessions can remain active or act on unintended page state. <br>
Mitigation: Inspect page state before secret-backed actions and terminate sandbox sessions when the task is complete. <br>
Risk: The CLI may optionally install persistent Toani instructions for Claude or Codex during onboarding. <br>
Mitigation: Decline optional skill installation unless persistent Toani instructions are desired in that agent environment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/toani/toani-vault-cli) <br>
- [Toani Vault CLI source](https://github.com/credbridge/credbridge/tree/main/cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may include CLI install commands, environment variable examples, smoke checks, credential metadata commands, and sandbox session commands.] <br>

## Skill Version(s): <br>
0.0.21 (source: artifact frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
