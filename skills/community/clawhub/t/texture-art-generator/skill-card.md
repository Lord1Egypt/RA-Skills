## Description:

Generate satisfying texture art and hyperrealistic material images from text prompts using the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blammectrappora](https://clawhub.ai/user/blammectrappora)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, designers, and developers use this skill to generate macro-style texture images for visual content, product backgrounds, and social media assets from text prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends user prompts and the API token to api.talesofai.com.

Mitigation: Use only prompts and credentials that are acceptable to share with that service, and use a low-privilege, revocable Neta/TalesOfAI token.

Risk: Passing the token directly with --token can expose it through shell history, process listings, or logs.

Mitigation: Avoid placing long-lived secrets directly on the command line; prefer short-lived or revocable tokens and clean any local logs or shell history that capture the token.

Risk: The documented npx install command is unpinned.

Mitigation: Prefer a pinned or otherwise verified install source before using the skill in a production workflow.

## Reference(s):

- [ClawHub Texture Art Generator release page](https://clawhub.ai/blammectrappora/skills/texture-art-generator)
- [Neta API token page](https://www.neta.art/open/)
- [Neta image generation endpoint](https://api.talesofai.com/v3/make_image)
- [Neta task polling endpoint](https://api.talesofai.com/v1/artifact/task/${taskUuid})

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text image URL printed to stdout with progress messages on stderr]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Neta API token; supports optional size and reference image UUID inputs.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
