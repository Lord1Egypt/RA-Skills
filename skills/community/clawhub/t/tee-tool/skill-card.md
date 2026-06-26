## Description: <br>
Read from stdin and write to both stdout and files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to preserve piped command output in a local file while still displaying the same output on screen. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper overwrites the selected output file and defaults to out.txt when no filename is provided. <br>
Mitigation: Use an explicit output path and verify that replacing the target file is acceptable before running the command. <br>
Risk: The artifact documents append, interrupt-ignore, and multi-file options that are not implemented by the included script. <br>
Mitigation: Do not rely on those options unless the implementation is updated and retested. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes stdin to stdout and one local file; defaults to out.txt when no filename is provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
