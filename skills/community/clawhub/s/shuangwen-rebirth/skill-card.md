## Description:

Chinese-language interactive fiction skill where users role-play as a reborn shuangwen protagonist, choose story branches or custom actions, and progress through themes such as CEO revenge, academic comeback, urban cultivation, and ancient power struggles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uccu](https://clawhub.ai/user/uccu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and Chinese-language interactive fiction players use this skill to run guided rebirth-story roleplay sessions with generated scene outcomes, recurring status panels, selectable options, custom actions, and save/load support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Chinese rebirth-roleplay trigger phrases may activate the skill when a user did not intend to start a session.

Mitigation: Confirm the user wants to enter the shuangwen roleplay mode before beginning or resuming a story.

Risk: Save/load behavior may store story progress in agent memory.

Mitigation: Treat saved story state as user-controlled session data and avoid including sensitive personal information in roleplay saves.

## Reference(s):

- [Shuangwen Theme Library](references/themes.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Chinese-language Markdown narrative text with status panels and numbered action options]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update story progress in agent memory when the user requests save/load behavior.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
