## Description: <br>
Split files into smaller pieces by size, line count, or number of chunks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to break large logs, datasets, or other files into smaller local parts for easier handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local splitter can overwrite existing output files when the chosen prefix collides with files in the output directory. <br>
Mitigation: Run it in a dedicated output folder or choose a unique prefix before splitting files. <br>
Risk: The documented -n option and exact line-count behavior are not reliable in the released implementation. <br>
Mitigation: Do not depend on -n or exact line-count splitting unless the implementation is fixed; verify output chunk counts and sizes after running. <br>


## Reference(s): <br>
- [Split Tool ClawHub release](https://clawhub.ai/dinghaibin/split-tool) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and local file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates numbered output files using the selected prefix.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
