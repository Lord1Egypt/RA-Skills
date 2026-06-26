## Description: <br>
CRM integration, lead tracking, outreach automation, and pipeline management for an AI sales assistant. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AlexeyVorobiev](https://clawhub.ai/user/AlexeyVorobiev) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Sales teams, operators, and agent users use this skill to track leads, manage pipeline status, prepare outreach and meeting materials, and generate sales reports from local Markdown templates and shell helpers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prospect and customer information may be stored in local plaintext files. <br>
Mitigation: Store only approved minimal fields, avoid sensitive customer data, and apply the user's normal local file access controls. <br>
Risk: Path-like company names can cause lead files to be written outside the intended leads folder. <br>
Mitigation: Do not use company names containing slashes, '..', or path-like text unless filename handling is fixed. <br>
Risk: CRM synchronization can transfer prospect or customer data to third-party systems. <br>
Mitigation: Use only approved CRM tools, least-privilege credentials, and data fields authorized for the target system. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AlexeyVorobiev/tmp-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands and local Markdown file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scripts create and update local sales workspace files under the user's home directory when run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
