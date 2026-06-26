## Description: <br>
Set up and use 1Password CLI (op). Use when installing the CLI, enabling desktop app integration, signing in (single or multi-account), or reading/injecting/running secrets via op. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[littlecrabzzz-alt](https://clawhub.ai/user/littlecrabzzz-alt) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to install, sign in to, and run 1Password CLI workflows for account checks and secret injection while following the documented guardrails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide access to sensitive 1Password vault data. <br>
Mitigation: Authorize only the intended 1Password account, specify the exact vault or item before access, and verify identity with op whoami before reading secrets. <br>
Risk: Secrets may be exposed in logs, chat, code, or temporary files. <br>
Mitigation: Avoid commands that print secret values, never paste secrets into logs or chat, and prefer op run or op inject over writing secrets to disk. <br>
Risk: An authenticated CLI session may remain active longer than intended. <br>
Mitigation: Run op commands in a dedicated tmux session and confirm that the session is closed after use. <br>


## Reference(s): <br>
- [1Password CLI get started](https://developer.1password.com/docs/cli/get-started/) <br>
- [ClawHub skill page](https://clawhub.ai/littlecrabzzz-alt/test-skill2123) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Command guidance is scoped to 1Password CLI setup, sign-in, access checks, and secret injection through a dedicated tmux session.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
