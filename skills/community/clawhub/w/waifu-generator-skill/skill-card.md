## Description:

Generate waifu generator ai image generator images with AI via the Neta AI image generation API (free trial at neta.art/open).

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomcarranzaem](https://clawhub.ai/user/tomcarranzaem)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to generate anime-style character images from text prompts, with optional size selection and reference-image UUID style inheritance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, optional reference image UUIDs, and the Neta API token are sent to api.talesofai.com.

Mitigation: Install only when that external API use is acceptable, avoid exposing long-lived tokens in shell history or logs, and rotate any token that may have been logged.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tomcarranzaem/skills/waifu-generator-skill)
- [Neta API Token Signup](https://www.neta.art/open/)
- [Neta Image Generation API Endpoint](https://api.talesofai.com/v3/make_image)
- [Neta Task Polling API Endpoint](https://api.talesofai.com/v1/artifact/task/${taskUuid})

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text image URL printed to stdout, with Markdown usage guidance in the skill documentation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Neta API token supplied with --token; supports optional --size and --ref arguments.]

## Skill Version(s):

3.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
