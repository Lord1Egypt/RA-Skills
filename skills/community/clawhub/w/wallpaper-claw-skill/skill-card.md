## Description:

Generates AI wallpaper images from text prompts through the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[barbaraledbettergq](https://clawhub.ai/user/barbaraledbettergq)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to request AI-generated wallpaper images from text prompts and receive an image URL. It supports selectable output sizes and optional reference image UUIDs for style inheritance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Neta/talesofai token can be exposed if pasted into shell history, logs, or shared transcripts.

Mitigation: Treat the token like a password, rotate it if exposure is suspected, and prefer a safer token mechanism if the publisher adds one.

Risk: Prompts are sent to an external image-generation API and may contain sensitive information.

Mitigation: Avoid entering sensitive prompts or private data into the generator.

Risk: The skill depends on a trusted external source and version.

Mitigation: Install only from the resolved ClawHub publisher and version you trust.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/barbaraledbettergq/skills/wallpaper-claw-skill)
- [Neta API access](https://www.neta.art/open/)
- [Neta/TalesofAI API endpoint](https://api.talesofai.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text URL or JSON status from Node scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Neta/talesofai token and may poll the external image-generation API before returning a result.]

## Skill Version(s):

2.1.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
