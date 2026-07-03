## Description: <br>
Backs up an OpenClaw `.openclaw` directory to Quark Netdisk on demand or through a daily cron job, excluding `node_modules` and browser cache. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[z157181773](https://clawhub.ai/user/z157181773) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to configure manual or scheduled backups of local OpenClaw workspace, memory, session, and configuration data to Quark Netdisk. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The backup can upload broad OpenClaw data, including workspace, memory, sessions, and configuration, to Quark cloud storage. <br>
Mitigation: Confirm included paths before use and exclude secrets, session files, and other sensitive data wherever possible. <br>
Risk: The workflow relies on a stored Quark session cookie for authentication. <br>
Mitigation: Protect the environment file containing `KUAKE_COOKIE`, restrict file permissions, and rotate or refresh the cookie when needed. <br>
Risk: A daily cron job can automatically upload backups without a fresh user review each time. <br>
Mitigation: Use automatic scheduling only when intended, review the cron entry, and monitor upload logs and remote backup contents. <br>


## Reference(s): <br>
- [kuake CLI setup reference](references/kuake-setup.md) <br>
- [Quark Netdisk](https://pan.quark.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash command examples and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May lead to creation of a compressed local backup archive and upload to Quark Netdisk when the provided shell commands are executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
