## Description: <br>
This skill helps agents discover, search, modify, validate, and import Unreal Engine DataTable JSON for AI Skills configurations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mufuxiao515-create](https://clawhub.ai/user/mufuxiao515-create) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical content teams use this skill to inspect and update Unreal Engine DataTable entries through their JSON representation, then validate and prepare the changes for import back into UE Editor. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can scan local project folders and inspect Unreal Engine DataTable JSON files. <br>
Mitigation: Prefer an explicit project root, table name, or JSON path so discovery is limited to the intended workspace. <br>
Risk: The skill can make real project-data changes. <br>
Mitigation: Review search results and proposed edits first, use dry-run for uncertain changes, and keep backups or source control available. <br>
Risk: Incorrect import targeting can update the wrong Unreal Engine DataTable asset. <br>
Mitigation: Run the UE import command only after confirming the target asset path, part number, and validation output. <br>


## Reference(s): <br>
- [AI Skills JSON Field Schema](references/field_schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON-focused guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce dry-run instructions, validation results, backup-aware edit guidance, and UE Editor import commands.] <br>

## Skill Version(s): <br>
1.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
