## Description:

Generate, edit, extend, and manage AI videos using OpenAI's Sora 2 API with marketing-ready prompt templates for product demos, social ads, brand spots, and launch teasers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jonathanlindsay](https://clawhub.ai/user/jonathanlindsay)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create, edit, extend, poll, download, list, and delete OpenAI Sora video jobs from a Python CLI. It also provides marketing-oriented prompt templates for product demos, social ads, brand spots, launch teasers, cinematic shots, and batch variants.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions ask users to run an unverified remote installer directly in a shell.

Mitigation: Install uv through a trusted package manager or verified release before running the skill.

Risk: The runtime OpenAI SDK dependency is unpinned.

Mitigation: Use a pinned OpenAI SDK version in an isolated environment.

Risk: Live API calls require an OPENAI_API_KEY and may incur usage charges.

Mitigation: Set OPENAI_API_KEY only in the local runtime environment and review prompts, model choices, durations, and pricing before live runs.

Risk: Delete and overwrite operations can affect existing generated assets.

Mitigation: Double-check video IDs before using delete, and verify output paths before using --force.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jonathanlindsay/skills/sora-video)
- [CLI Reference](references/cli.md)
- [Sora Video API quick reference](references/video-api.md)
- [Prompting best practices (Sora)](references/prompting.md)
- [Sample prompts](references/sample-prompts.md)
- [Troubleshooting](references/troubleshooting.md)
- [Cinematic shot templates](references/cinematic-shots.md)
- [Product Demo Templates](templates/product-demo.md)
- [Social Ad Templates](templates/social-ads.md)
- [Brand Spot Templates](templates/brand-spots.md)
- [Launch Teaser Templates](templates/launch-teaser.md)
- [OpenAI API keys](https://platform.openai.com/api-keys)
- [OpenAI API pricing](https://openai.com/api/pricing/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, Python CLI usage, prompt templates, and optional JSON output files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live runs require a customer-provided OPENAI_API_KEY; generated video, thumbnail, and spritesheet assets are retrieved through the Sora API.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, package.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
