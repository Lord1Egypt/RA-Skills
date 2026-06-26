## Description: <br>
Minimal secure secret handoff. Zero external deps. Human opens browser form, submits secret, agent receives it via temp file. Secret NEVER appears in stdout/logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BitBrujo](https://clawhub.ai/user/BitBrujo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to receive a sensitive value from a human through a temporary local web form and read it from a permission-restricted file instead of exposing the secret in command output or chat logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The temporary HTTP server binds to all interfaces and prints network URLs, so secrets can be submitted from the local network if the URL is shared or discovered. <br>
Mitigation: Use the localhost URL only, avoid shared or untrusted networks, and stop the server after a single handoff. <br>
Risk: The skill writes sensitive values to a temporary file. <br>
Mitigation: Use short-lived scoped tokens when possible, keep the generated file permissions restrictive, read the file only for the intended command, and delete it immediately after use. <br>
Risk: Shell one-liners that pipe the secret through xargs can expose or mishandle values with shell-sensitive characters. <br>
Mitigation: Avoid the xargs one-liner and prefer assigning the file content to a quoted shell variable before invoking the target command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/BitBrujo/side-peace) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces instructions for running a local Node.js handoff server and handling the resulting temporary secret file.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
