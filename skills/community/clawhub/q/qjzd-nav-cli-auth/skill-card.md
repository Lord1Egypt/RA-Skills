## Description: <br>
Use when working with QJZD Nav CLI login, bearer token auth, profile setup, profile switching, current profile inspection, or fixing missing keyring credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nqdy666](https://clawhub.ai/user/nqdy666) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to set up and troubleshoot QJZD Nav CLI authentication, manage auth profiles, inspect current credentials, and prepare the CLI for content or operations commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The login flow may expose a real password if it is placed directly in a shell command. <br>
Mitigation: Prefer an interactive, stdin, or secret-manager workflow when available, and avoid storing passwords in shell history or shared logs. <br>
Risk: Profile deletion and profile switching can affect production CLI access. <br>
Mitigation: Confirm the current profile and target environment before deleting, forcing, or switching profiles. <br>
Risk: Authentication depends on the qjzd-nav CLI and the configured QJZD Nav server. <br>
Mitigation: Install and use this skill only when the CLI and configured server URL are trusted. <br>


## Reference(s): <br>
- [QJZD Nav service](https://nav.qjzd.online) <br>
- [ClawHub skill page](https://clawhub.ai/nqdy666/qjzd-nav-cli-auth) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.3.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
