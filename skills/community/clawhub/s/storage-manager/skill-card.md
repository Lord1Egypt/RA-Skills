## Description: <br>
Storage Manager helps agents manage item locations in Feishu Bitable with smart location matching, item search, location updates, and optional item and location image uploads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ruoruochen](https://clawhub.ai/user/ruoruochen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and their agents use the skill to record where household or personal items are stored, search those records, update locations, and attach photos in Feishu Bitable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence reports real-looking embedded Feishu credentials and table identifiers. <br>
Mitigation: Remove embedded credentials and table identifiers, rotate any exposed values, require user-provided configuration, and fail closed when credentials are missing. <br>
Risk: The skill can perform remote reads, writes, and uploads involving item names, locations, and selected photos. <br>
Mitigation: Use a dedicated low-privilege Feishu app and table, and make users aware that item, location, and photo data may be uploaded to Feishu. <br>
Risk: Automatic location matching can create or update persistent remote records without an explicit confirmation step. <br>
Mitigation: Require review or confirmation before remote writes when a location is newly created, changed, or matched near the similarity threshold. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ruoruochen/storage-manager) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown guidance with command examples and JSON-like result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read, create, update, and upload item, location, and selected photo data in Feishu when executed.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
