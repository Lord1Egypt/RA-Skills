## Description:

Analyzes videos with the NanoPhoto.AI Video Reverse Prompt API to produce shot-by-shot breakdowns, reverse prompts, and AI-ready visual descriptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sctc888-hub](https://clawhub.ai/user/sctc888-hub)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and content teams use this skill to analyze authorized YouTube, MP4 URL, or local MP4 video sources and turn them into structured shot breakdowns and prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Videos, URLs, and local files are sent to NanoPhoto.AI for processing.

Mitigation: Use the skill only for media the user is authorized to upload and avoid confidential media unless third-party processing is acceptable.

Risk: API keys may be exposed if passed on the command line or pasted into chat.

Mitigation: Configure NANOPHOTO_API_KEY through the platform or environment and avoid the --api-key option when possible.

Risk: API calls consume NanoPhoto.AI credits and local uploads are limited to MP4 files up to 30 MB.

Mitigation: Confirm the intended video source and constraints before calling the API, and use the bundled helper for local MP4 uploads.

## Reference(s):

- [Video Reverse Prompt API Reference](references/api.md)
- [NanoPhoto.AI homepage](https://nanophoto.ai)
- [NanoPhoto.AI API key settings](https://nanophoto.ai/settings/apikeys)
- [ClawHub skill page](https://clawhub.ai/sctc888-hub/skills/reverseprompt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Streaming plain text containing Markdown tables and narrative guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires NANOPHOTO_API_KEY; supports YouTube links, direct MP4 URLs, and local MP4 files up to 30 MB.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
