## Description: <br>
Manage YouTrack issues, projects, and workflows via CLI for creating, updating, searching, commenting, listing projects, checking states, and automating issue workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iAhmadZain](https://clawhub.ai/user/iAhmadZain) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and support teams use this skill to manage YouTrack projects and issues from an agent workflow, including querying work, updating fields, adding comments, and producing reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill references ytctl, but that CLI is not packaged in the artifact. <br>
Mitigation: Verify the available ytctl implementation and commands before installing or executing the skill. <br>
Risk: Create, update, assign, comment, and bulk commands can change multiple YouTrack issues. <br>
Mitigation: Use a least-privilege token, narrow queries, dry-run previews, and explicit confirmation before multi-issue changes. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/iAhmadZain/youtrack) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text, JSON] <br>
**Output Format:** [Markdown guidance with bash examples; command output may be table text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires jq and curl; uses a YouTrack URL and token supplied by the user environment or config.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
