## Description:

Helps agents manage Vibbit product and creative libraries, research products, and plan, generate, localize, and revise marketing images, video, audio, subtitles, and comics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zgissing](https://clawhub.ai/user/zgissing)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, marketers, and developers use this skill to manage product and creative assets, produce ecommerce imagery and advertising videos, and adapt or localize media through Vibbit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic updates use an unpinned installer that can change the skill before use.

Mitigation: Disable automatic updates or review updates before running the skill.

Risk: The skill can access API credentials, local creative files, and product or media data sent to Vibbit.

Mitigation: Trust the publisher and Vibbit before use, store keys in a host secret manager, and avoid submitting confidential media unless Vibbit processing is acceptable.

Risk: Product deletion and paid generation requests can have irreversible or billable effects.

Mitigation: Confirm deletions and paid generation requests before execution.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zgissing/skills/vibbit-skills)
- [Vibbit API documentation](https://vibbit.apifox.cn/)
- [Skill capabilities and workflows](references/catalog.md)
- [Authentication and environment](references/runtime/authentication.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance, Media files]

**Output Format:** [Markdown guidance, commands, and generated media files or links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Media generation and account operations may require Vibbit credentials and credits.]

## Skill Version(s):

2.18.0 (source: frontmatter, package.json, ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
