## Description:

Generates stained-glass-style art and illustrations from text prompts using the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blammectrappora](https://clawhub.ai/user/blammectrappora)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to request stained-glass-style images such as portraits, animals, landscapes, and decorative panels from text prompts, with optional size and reference-image controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles API tokens and prompt data through the Neta image generation flow with incomplete provider disclosure.

Mitigation: Use only non-sensitive prompts, verify that the token is intended for use with api.talesofai.com, and prefer scoped, revocable tokens.

Risk: The documented command-line token flag can expose real tokens through shell history or process listings.

Mitigation: Avoid placing production tokens directly on the command line; use safer local secret handling where possible.

Risk: The installation guidance includes an unpinned npx command.

Mitigation: Prefer a pinned package version or the ClawHub-native install path before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/blammectrappora/skills/stained-glass-art-generator)
- [Neta API token setup](https://www.neta.art/open/)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text image URL with command-line status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Neta API token; supports optional size and reference image UUID arguments.]

## Skill Version(s):

1.0.0 (source: release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
