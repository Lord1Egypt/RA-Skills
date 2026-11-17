## Description:

Render a video from a script using only the media assets the caller provides, with no stock visuals, for branded content where every frame must be on-brand.

This skill is ready for commercial/non-commercial use.

## Publisher:

[api00](https://clawhub.ai/user/api00)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to create Revid script-to-video renders when they already have public brand media assets and need to prevent stock visuals from being mixed in.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scripts, media URLs, and authenticated render requests are sent to Revid.

Mitigation: Use the skill only when that external processing is acceptable for the content being rendered.

Risk: Public media URLs can expose private or sensitive assets.

Mitigation: Provide intentionally public links only, or use signed URLs only when their exposure and expiration behavior are acceptable.

Risk: The Revid API key could authorize unwanted render activity if leaked.

Mitigation: Keep REVID_API_KEY scoped, protected, and out of committed files or shared logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/api00/skills/revid-script-with-custom-media)
- [Publisher profile](https://clawhub.ai/user/api00)
- [Revid render API endpoint](https://www.revid.ai/api/public/v3/render)
- [Example branded script payload](examples/branded-script.json)
- [Example render runner](examples/run.sh)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, API Calls]

**Output Format:** [Markdown guidance with JSON payload examples and bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Revid render requests that require REVID_API_KEY and user-provided public media URLs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
