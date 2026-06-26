## Description: <br>
x-df helps agents use the x-cmd `x df` module to view disk usage and mount information across TSV, CSV, TUI, and raw output modes with filesystem type detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edwinjhlee](https://clawhub.ai/user/edwinjhlee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agents use this skill to inspect local disk capacity, filesystem type, mount point, and mount attribute information through the x-cmd `x df` module. It supports interactive terminal viewing and structured TSV or CSV output for scripting and data processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the underlying command may reveal local disk names, mount points, filesystem types, usage values, and mount options. <br>
Mitigation: Use the skill only where local system metadata disclosure is acceptable, and review command output before sharing it outside the current environment. <br>
Risk: The skill depends on the separate x-cmd tool, which must be installed before use. <br>
Mitigation: Install x-cmd only from a trusted source and verify the installation path before asking an agent to run `x df` commands. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/edwinjhlee/x-df) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and command outputs in TUI, TSV, CSV, or raw text formats.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The underlying x-cmd module may expose local filesystem names, mount points, filesystem types, usage values, and mount attributes.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
