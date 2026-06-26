## Description: <br>
Interact with the FamilyWall family organization platform to manage calendar events, shopping lists, tasks, family messaging, member locations, meal plans, recipes, the family wall/feed, and media file downloads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snowsand-enterprises](https://clawhub.ai/user/snowsand-enterprises) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to operate a FamilyWall household account from the command line: checking calendars and member locations, managing lists and meals, reading or sending messages, reviewing wall posts, and downloading attached media. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access private household data, including locations, messages, lists, recipes, and media. <br>
Mitigation: Install and invoke it only for a trusted FamilyWall account, scope prompts narrowly, and avoid broad automations that could expose family data unintentionally. <br>
Risk: Media download commands can write files to local paths. <br>
Mitigation: Download media into a dedicated directory and review requested filenames and overwrite behavior before running download or download-all commands. <br>
Risk: The skill requires sensitive FamilyWall credentials. <br>
Mitigation: Store credentials only in the expected local environment file or secret store, keep them out of prompts and logs, and rotate them if exposed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/snowsand-enterprises/snowsand-familywall) <br>
- [FamilyWall API Reference](https://snowsand.atlassian.net/wiki/spaces/SD/pages/38436865) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, code, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FamilyWall email/password environment variables and can write downloaded media files to local paths.] <br>

## Skill Version(s): <br>
1.3.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
