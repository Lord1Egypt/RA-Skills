## Description: <br>
Deep security analysis of an individual skill before installation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[itsnishi](https://clawhub.ai/user/itsnishi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill to inspect a skill directory before installation or review, producing severity-ranked findings and recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Package names found during scans may be checked against PyPI or npm, which can expose confidential internal dependency names. <br>
Mitigation: Run the skill only on directories intended for review, and avoid scanning private skills with confidential dependency names when registry lookups are unacceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/itsnishi/scan-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with severity-ranked findings and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs against one skill directory path at a time; package names found during scans may be checked against PyPI or npm.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
