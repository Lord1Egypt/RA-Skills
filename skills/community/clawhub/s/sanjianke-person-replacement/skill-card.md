## Description:

Helps agents submit and track person-replacement video jobs using a reference image and input video through the a7w API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2253128](https://clawhub.ai/user/2253128)

### License/Terms of Use:

MIT

## Use Case:

Creators and developers use the skill to submit a reference image and source video for person replacement, then check job status and retrieve the resulting video link.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The client supports more API actions than person replacement and can send the API key to a configurable host.

Mitigation: Use only a trusted api.a7w.cn host; avoid host overrides unless you control the endpoint, and remove any saved host override before use.

Risk: Public image and video URLs can expose sensitive likenesses or footage.

Mitigation: Get consent before processing faces or video, and use media hosting with an appropriate access and retention plan.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/2253128/skills/sanjianke-person-replacement)
- [a7w API and account setup](https://api.a7w.cn/)
- [Getting started](references/getting-started.md)
- [Submit API documentation](references/api-submit.md)
- [Query API documentation](references/api-query.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, JSON]

**Output Format:** [Markdown guidance and JSON task status or result URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [An asynchronous task may return a video URL when complete; requires an a7w API key and publicly accessible input media URLs.]

## Skill Version(s):

1.0.7 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
