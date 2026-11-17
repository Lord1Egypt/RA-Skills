## Description:

Generate surreal AI art from text prompts in dreamlike, absurdist, Dali-inspired, Magritte-inspired, and abstract surreal styles using the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omactiengartelle](https://clawhub.ai/user/omactiengartelle)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creators use this skill to generate surreal image concepts, social visuals, album-cover ideas, gallery-print concepts, and other creative art outputs from text prompts with optional size and reference-image controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends image prompts, API tokens, selected image sizes, and optional reference image UUIDs to api.talesofai.com.

Mitigation: Avoid sensitive prompts or confidential reference identifiers, use the service only where third-party API processing is acceptable, and review the provider's terms before use.

Risk: Passing real API tokens directly on a command line can expose them through shell history or process listings.

Mitigation: Prefer expanding the token from a protected environment variable and rotate any token that was previously exposed on a command line.

Risk: Install guidance includes unpinned package-manager installation.

Mitigation: Prefer a ClawHub install or a pinned installer version before using the skill in a controlled environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/omactiengartelle/skills/surreal-art-generator)
- [Neta API Token Access](https://www.neta.art/open/)
- [Tales of AI API Endpoint](https://api.talesofai.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and command-line guidance; the runtime script prints a direct image URL on success.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Neta API token, sends prompts and selected options to api.talesofai.com, and may use an optional reference image UUID for style inheritance.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
