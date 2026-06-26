## Description: <br>
Local-first encrypted secret management with the tene CLI for safely handling secrets, API keys, credentials, tokens, .env files, and command execution that needs injected environment variables. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tomo-kay](https://clawhub.ai/user/tomo-kay) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to guide AI coding agents through Tene secret-management workflows while avoiding plaintext secret exposure in chat, logs, files, shell history, or process arguments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is intended for secret-management workflows, so careless command approval could expose or alter sensitive project credentials. <br>
Mitigation: Review exact commands before execution, especially imports, deletes, deploys, and production runs. <br>
Risk: Pasting secret values, master passwords, or recovery phrases into chat would place sensitive material in the conversation context. <br>
Mitigation: Enter secrets only through local Tene prompts or stdin workflows outside the chat transcript. <br>
Risk: Migrating from plaintext .env files can cause data loss if the import is wrong and the file is deleted too early. <br>
Mitigation: Verify imported key names and keep a temporary backup before deleting plaintext .env files. <br>


## Reference(s): <br>
- [Tene homepage](https://tene.sh) <br>
- [Tene installer metadata](https://tene.sh/install.sh) <br>
- [ClawHub skill page](https://clawhub.ai/tomo-kay/tene-cli) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and concise safety guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill is documentation-only and instructs agents to avoid printing, exporting, or reading plaintext secrets.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
