## Description: <br>
Turbine is packaged as a turbine performance calculator, but server security evidence identifies its behavior as a local command-line entry tracker. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain1](https://clawhub.ai/user/bytesagain1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can run the bundled shell commands to add, list, search, remove, export, and summarize local entries stored under ~/.turbine. Review before use because the security evidence says the published purpose does not match the artifact behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill claims to be a turbine calculator but behaves as a local entry tracker. <br>
Mitigation: Review the shell script behavior before installation and do not rely on it for turbine engineering calculations. <br>
Risk: User-provided entries are retained locally and can be exported or deleted by the script. <br>
Mitigation: Avoid entering sensitive information and set TURBINE_DIR to a controlled location when local retention matters. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/bytesagain1/turbine) <br>
- [Publisher Homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Files] <br>
**Output Format:** [Plain text command output, JSONL data files, and optional JSON or CSV export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores entries under ~/.turbine by default; TURBINE_DIR can change the data directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
