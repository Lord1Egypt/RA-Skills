## Description: <br>
Generate release notes from git commit history using the Conventional Commits convention, with categorized Markdown output, date or version filtering, and optional file output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rogue-agent1](https://clawhub.ai/user/rogue-agent1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release managers use this skill to summarize repository commit history into categorized release notes for changelogs, release preparation, or version announcements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads commit history from repositories the user points it at. <br>
Mitigation: Run it only on repositories whose history you are authorized to inspect. <br>
Risk: The output option writes a generated Markdown file and may overwrite an existing file at the chosen path. <br>
Mitigation: Choose the output path deliberately and check for existing files before using the output option. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rogue-agent1/releasenotes) <br>
- [Publisher profile](https://clawhub.ai/user/rogue-agent1) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Files, Shell commands] <br>
**Output Format:** [Markdown release notes printed to console or written to a user-selected Markdown file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Categorizes commits by Conventional Commits type and includes abbreviated commit hash and author.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
