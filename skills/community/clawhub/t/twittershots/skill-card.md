## Description:

Generate high-quality screenshots of Twitter/X posts using the TwitterShots API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xinhua](https://clawhub.ai/user/0xinhua)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use TwitterShots to turn Twitter/X URLs or tweet IDs into PNG, SVG, or HTML screenshots for sharing, archiving, and social-media publishing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tweet IDs, rendering options, optional background image URLs, and the TwitterShots API key are sent to a third-party service.

Mitigation: Use the skill only when that disclosure is acceptable, and avoid sending sensitive or private tweet references or background image URLs.

Risk: Passing the API key with --api-key can expose it through shell history or process metadata.

Mitigation: Store TWITTERSHOTS_API_KEY in a protected environment or secret manager instead of passing the key directly on the command line.

## Reference(s):

- [TwitterShots skill on ClawHub](https://clawhub.ai/0xinhua/skills/twittershots)
- [Publisher profile](https://clawhub.ai/user/0xinhua)
- [Project homepage](https://github.com/twittershots/skills)
- [TwitterShots API key settings](https://twittershots.com/settings/keys)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; generated screenshots are PNG, SVG, HTML, or URL outputs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TWITTERSHOTS_API_KEY and sends tweet IDs plus rendering options to the TwitterShots API.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
