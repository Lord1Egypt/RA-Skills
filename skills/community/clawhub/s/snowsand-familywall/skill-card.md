## Description:

Interact with the FamilyWall family organization platform to manage calendars, lists, tasks, messages, member locations, meal plans, recipes, wall/feed posts, and media downloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snowsand-enterprises](https://clawhub.ai/user/snowsand-enterprises)

### License/Terms of Use:

MIT-0

## Use Case:

FamilyWall users and authorized assistants use this skill to read and update family organization data, including events, lists, messages, member locations, meals, recipes, wall posts, and media attachments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Media download by URL can send FamilyWall session credentials to an arbitrary URL.

Mitigation: Use media download --url only with URLs copied directly from FamilyWall media listings, and prefer media-ID downloads when possible.

Risk: Media download output paths can write files outside the intended download area.

Mitigation: Download media only into a dedicated empty directory and review output paths before use.

Risk: Command outputs can expose private family data such as locations, member details, messages, and media metadata.

Mitigation: Run the skill only in trusted environments and keep generated outputs, logs, and downloaded files access-restricted.

## Reference(s):

- [FamilyWall API Reference](https://snowsand.atlassian.net/wiki/spaces/SD/pages/38436865)
- [FamilyWall Skill Page](https://clawhub.ai/snowsand-enterprises/skills/snowsand-familywall)
- [FamilyWall Publisher Profile](https://clawhub.ai/user/snowsand-enterprises)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands; CLI responses are JSON and media downloads are files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses FamilyWall account credentials from environment variables and can read or modify private family data.]

## Skill Version(s):

1.3.0 (source: SKILL.md frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
