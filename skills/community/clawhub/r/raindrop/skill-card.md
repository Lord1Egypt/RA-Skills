## Description: <br>
Search, list, and manage Raindrop.io bookmarks via CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[velvet-shark](https://clawhub.ai/user/velvet-shark) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to search, list, add, update, delete, move, and bulk-organize bookmarks in their Raindrop.io library from an agent-driven CLI workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Raindrop.io token that can access and manage the user's bookmark account. <br>
Mitigation: Pass RAINDROP_TOKEN through a trusted environment or keep ~/.config/raindrop.env private with restrictive permissions and only a simple token assignment. <br>
Risk: Write operations such as delete, update, move, and bulk-move can change or remove bookmarks. <br>
Mitigation: Confirm bookmark IDs and collection targets before running destructive or bulk modification commands. <br>


## Reference(s): <br>
- [Raindrop.io API documentation](https://developer.raindrop.io/) <br>
- [Raindrop.io Bookmarks on ClawHub](https://clawhub.ai/velvet-shark/raindrop) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Raindrop.io API token and local command dependencies: bash, curl, jq, and bc.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
