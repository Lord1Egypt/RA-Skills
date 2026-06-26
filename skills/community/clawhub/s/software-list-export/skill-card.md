## Description: <br>
Export installed software to CSV with versions and likely download URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[auto-dog](https://clawhub.ai/user/auto-dog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to prepare a machine inventory or reinstall checklist before migration to a new computer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A software inventory can reveal personal, workplace, or security-sensitive details about the machine. <br>
Mitigation: Review the generated CSV before sharing it and remove entries or metadata that should not leave the machine. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/auto-dog/software-list-export) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files] <br>
**Output Format:** [CSV file plus a brief text message with the saved path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CSV columns are name, version, download_url, and comments; comments should identify uncertainty in source data or reinstall URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
