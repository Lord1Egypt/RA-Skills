## Description: <br>
Executes common Windows system commands and aliases from OpenClaw, returning formatted system, network, process, and diagnostic output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ljr287404428](https://clawhub.ai/user/ljr287404428) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect Windows host state, troubleshoot networking, list processes, and run configured diagnostic commands from an agent session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run Windows shell commands with the privileges of the hosting process. <br>
Mitigation: Install only where agent shell access is intended, review configured aliases, and restrict use to trusted users and hosts. <br>
Risk: Command output can expose sensitive host, network, process, account, or service information. <br>
Mitigation: Treat results as sensitive operational data and avoid sharing logs or transcripts outside the intended security boundary. <br>
Risk: High-impact commands may write files, terminate processes, change services, or otherwise affect system state when confirmed. <br>
Mitigation: Avoid `--yes`, redirection, and destructive commands unless the operator has reviewed the exact command and accepted the system impact. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ljr287404428/system-cmd) <br>
- [Command reference](references/commands.md) <br>
- [Usage examples](references/usage_examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text command output with status, errors, and formatted Windows command results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include sensitive host, network, process, account, or service details and may be truncated for length.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
