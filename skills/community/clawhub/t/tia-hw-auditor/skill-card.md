## Description: <br>
Use TIA Openness to compare hardware and I/O configuration between field and master backups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cjmore66](https://clawhub.ai/user/cjmore66) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Automation engineers and maintenance teams use this skill to compare Siemens TIA Portal field and master backups, detect hardware and I/O changes, and return audit results for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access network backup paths and run an external audit script. <br>
Mitigation: Use a vetted audit script from a fixed trusted location and restrict the agent to read-only allowlisted backup paths. <br>
Risk: Heartbeat automation could trigger audits without appropriate operator control. <br>
Mitigation: Allow heartbeat automation only from trusted operators or systems and review generated CSV and JSON before acting on reported changes. <br>


## Reference(s): <br>
- [TIA Hardware Auditor Scripts](Scripts/README.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/cjmore66/tia-hw-auditor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [CSV change report and JSON summary, with concise text or markdown guidance for the calling agent] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces hardware-diff.csv and summary.json from compared .zap18 backups when the external audit script is available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
