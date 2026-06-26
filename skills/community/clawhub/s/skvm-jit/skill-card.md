## Description: <br>
Triggers `skvm jit-optimize` with post-task evidence to generate a reviewable optimization proposal for a skill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lec77](https://clawhub.ai/user/lec77) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill after a skill-driven task fails, ends partially, or exposes confusing skill instructions. It helps collect evidence and launch an optimization proposal that can be reviewed before accepting any changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may require sensitive credentials for optimizer execution. <br>
Mitigation: Grant only the credentials needed for the optimization run, and inspect requested tools, environment variables, install steps, and commands before granting access. <br>
Risk: Task logs or optimization reports can accidentally include sensitive information. <br>
Mitigation: Redact secrets and private data before preparing optimizer input. <br>
Risk: Generated proposals can introduce incorrect or misleading changes to skill instructions. <br>
Mitigation: Review and scan each proposal before accepting or deploying it. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/lec77/skvm-jit) <br>
- [SkVM Installer](https://skillvm.ai/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a proposal id for later review; does not accept or deploy proposals by itself.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
