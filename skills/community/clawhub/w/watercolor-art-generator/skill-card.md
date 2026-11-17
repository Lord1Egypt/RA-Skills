## Description:

AI watercolor art generator that creates watercolor paintings, portraits, and illustrations from text prompts using the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blammectrappora](https://clawhub.ai/user/blammectrappora)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate watercolor-style images from text prompts through the Neta API, with optional image sizing and reference-image style inheritance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, reference image UUIDs, and the Neta token are sent to a remote API.

Mitigation: Avoid confidential prompts or reference content, pass tokens only in trusted environments, and rotate tokens if command history or process listings may have exposed them.

Risk: The documented npx install command is unpinned.

Mitigation: Prefer the ClawHub install path or a pinned, verified installer before deploying the skill.

Risk: Image generation depends on the external API completing successfully and returning an image URL.

Mitigation: Handle timeout, moderation, and missing-result failures in the calling workflow, and retry with adjusted prompts when appropriate.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/blammectrappora/skills/watercolor-art-generator)
- [Neta API Token and Access](https://www.neta.art/open/)
- [Tales of AI Image Generation API Endpoint](https://api.talesofai.com/v3/make_image)

## Skill Output:

**Output Type(s):** [text]

**Output Format:** [Plain text URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a direct image URL after polling the remote image-generation API.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
