## Description:

Create vertical scarcity-mystery shorts with option teases, a user-confirmed final reveal, timed English captions, and WeryAI video generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoucdr](https://clawhub.ai/user/zoucdr)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and agents use this skill to plan and generate vertical WeryAI shorts that ask what is scarcer than money, tease two or three candidate answers, and reveal a concise final answer with timed English captions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local image paths can be read and uploaded to WeryAI file storage.

Mitigation: Prefer public HTTPS image URLs; use local paths only after reviewing the helper script and confirming the exact files are intended for upload.

Risk: The WERYAI_API_KEY authorizes paid network generation and upload requests.

Mitigation: Use a scoped or short-lived API key where possible and confirm the prompt, model, duration, and image inputs before submission.

Risk: Generated hook content may be mistaken for finance or therapy advice.

Mitigation: Keep outputs framed as short-form creative hook content and avoid presenting scarcity claims as professional advice.

## Reference(s):

- [ClawHub Skill: scarcest-not-money-video-gen](https://clawhub.ai/zoucdr/skills/scarcest-not-money-video-gen)
- [WeryAI Video API Reference](resources/WERYAI_VIDEO_API.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with CLI JSON payloads and final video links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WERYAI_API_KEY and Node.js 18+; execution may submit paid network video generation jobs.]

## Skill Version(s):

1.0.0 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
