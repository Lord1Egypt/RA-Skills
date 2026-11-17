## Description:

Generate videos with the NanoPhoto.AI Sora 2 API in text-to-video or image-to-video mode, including submission, status checks, and optional polling through the bundled script.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nanophotohq](https://clawhub.ai/user/nanophotohq)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to generate NanoPhoto.AI Sora 2 videos from text prompts or public image URLs, then check task status and return final video details when available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, public image URLs, task IDs, and the NanoPhoto API key are sent to NanoPhoto.AI.

Mitigation: Use the skill only for data intended for NanoPhoto.AI, avoid private or sensitive images, and configure NANOPHOTO_API_KEY through the platform secure environment-variable setting.

Risk: Passing the API key on the command line can expose it through shell history or process logs on shared systems.

Mitigation: Prefer the platform secure environment variable or injected NANOPHOTO_API_KEY instead of --api-key.

Risk: Image-to-video mode requires public image URLs, so local files and base64 images are not accepted.

Mitigation: Provide only authorized public URLs and confirm that the user is comfortable sending those URLs to the service.

## Reference(s):

- [Sora 2 Video Generation API Reference](references/api.md)
- [NanoPhoto.AI homepage](https://nanophoto.ai)
- [NanoPhoto API key settings](https://nanophoto.ai/settings/apikeys)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return submitted task IDs, progress/status responses, final video URLs, generation time, and credits used when available.]

## Skill Version(s):

1.2.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
