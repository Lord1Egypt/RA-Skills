## Description: <br>
Work safely with files inside the OpenClaw workspace sandbox for listing directories, reading text files, writing text files, and searching files by name inside ~/.openclaw/workspace only. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EcosincronIA](https://clawhub.ai/user/EcosincronIA) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to inspect, search, read, and write text files within a declared workspace sandbox. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The write-file command can replace file contents inside the configured workspace sandbox. <br>
Mitigation: Confirm that /home/cmart/.openclaw/workspace is the intended sandbox and review write-file uses before execution. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs and commands are scoped to paths under the configured OpenClaw workspace sandbox.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
