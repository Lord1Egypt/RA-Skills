## Description: <br>
Use TIA Openness to compare latest site backup against yesterday's baseline with focus on process control logic. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cjmore66](https://clawhub.ai/user/cjmore66) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Field engineers and controls engineers use this skill to compare Siemens TIA Portal site backup archives against a recent baseline and identify significant process-control logic changes, including PID, safety, sequence, and alarm changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks an agent to locate sensitive site backup archives and run an external diff script, which could expose process-control and safety logic or execute unreviewed tooling. <br>
Mitigation: Use explicit baseline and new .zap18 paths, restrict access to a read-only folder containing only those backups, run only a reviewed trusted PowerShell diff script, and treat the JSON output as sensitive operational information. <br>


## Reference(s): <br>
- [TIA Commissioning Delta Scripts](Scripts/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [JSON with concise agent-facing guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes summary counts, change lists with risk levels, block names, and descriptions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
