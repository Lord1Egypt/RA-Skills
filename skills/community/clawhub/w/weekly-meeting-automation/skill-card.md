## Description: <br>
Automates a weekly meeting Excel follow-up workflow by finding the latest workbook, creating a dated copy, updating the date column, and sending the file to a configured Meixin work group. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paudyyin](https://clawhub.ai/user/paudyyin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees responsible for Smart Equipment Institute weekly meetings use this skill to prepare a dated Excel follow-up sheet and send it to the designated Meixin work group on a weekly schedule. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically modify and upload a local business Excel file on a weekly schedule. <br>
Mitigation: Require preview or approval before sending, verify the recipient group, and narrow the watched directory to the intended workbook location. <br>
Risk: The reviewed package references PowerShell and batch scripts that are not included in the artifact. <br>
Mitigation: Inspect the local scripts before installation and pin expected paths or hashes before allowing scheduled execution. <br>
Risk: The workflow depends on mx-im authorization and file-upload permissions. <br>
Mitigation: Use a least-privileged account and confirm Meixin upload and group-message permissions before enabling the cron task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/paudyyin/weekly-meeting-automation) <br>
- [Artifact skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or chat text with command snippets, configuration details, and execution status.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify a dated Excel workbook and send it to a configured group when the referenced local scripts and account permissions are present.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
