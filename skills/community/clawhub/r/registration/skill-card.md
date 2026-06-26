## Description: <br>
Manage registration records and attendee data. Use when logging sign-ups, checking capacity, converting export formats, generating confirmation reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this skill to log registration or attendee-related entries, inspect recent activity, search local records, and export local records for backup or review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Registration or attendee details are stored locally under ~/.local/share/registration. <br>
Mitigation: Install only if local storage of those details is acceptable, and manage or remove the local data directory according to the user's data-retention needs. <br>
Risk: Some commands are vague or partly broken and may not perform real capacity checks, conversions, or reports. <br>
Mitigation: Verify the installed command matches the reviewed script and test each required command before relying on its output. <br>


## Reference(s): <br>
- [ClawHub Registration Skill Page](https://clawhub.ai/ckchzh/registration) <br>
- [BytesAgain Homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files] <br>
**Output Format:** [Plain text command output with optional JSON, CSV, or TXT export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores local records and activity logs under ~/.local/share/registration.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata; artifact frontmatter and script report 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
