## Description:

AI webtoon character generator that creates manhwa-style portraits, Korean comic characters, and webtoon OCs with clean line art, expressive eyes, and vibrant colors via the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omactiengartelle](https://clawhub.ai/user/omactiengartelle)

### License/Terms of Use:

MIT-0

## Use Case:

External users, creators, and developers use this skill to generate webtoon and manhwa-style character images from text prompts, with optional size selection and reference-image style inheritance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, reference IDs, and generation settings are sent to an external Neta/TalesOfAI service.

Mitigation: Do not include confidential, personal, or proprietary content in prompts or reference IDs unless that external service is approved for the intended use.

Risk: Passing long-lived API tokens on the command line can expose them through shell history or logs.

Mitigation: Use short-lived or revocable Neta API tokens where possible, avoid storing tokens in shared logs, and rotate tokens if exposure is suspected.

Risk: Unpinned installs may change behavior when upstream skill releases change.

Mitigation: Prefer a pinned or ClawHub-managed install path for production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/omactiengartelle/skills/webtoon-character-generator)
- [Neta AI token and API access](https://www.neta.art/open/)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Text]

**Output Format:** [Plain text image URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Neta API token and sends prompts, optional reference IDs, and generation settings to the external Neta/TalesOfAI service.]

## Skill Version(s):

1.0.1 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
