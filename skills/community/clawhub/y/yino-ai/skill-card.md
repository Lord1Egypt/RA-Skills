## Description:

Generate images and videos using yino.ai for Seedream image generation, Veo video generation, and related media-generation tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hackerqed](https://clawhub.ai/user/hackerqed)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent discover yino.ai media-generation capabilities, submit authenticated image or video generation jobs, poll asynchronous results, upload source media, and organize multi-generation projects for preview.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API-key handling could expose YINO_API_KEY if the value is printed, logged, or pasted into chat.

Mitigation: Verify that the environment variable is set without revealing its value, avoid echoing the secret, and send it only in the Authorization header to trusted yino.ai endpoints.

Risk: Changing YINO_API_BASE_URL away from the official HTTPS origin could send credentials and uploaded media to an untrusted endpoint.

Mitigation: Keep YINO_API_BASE_URL on https://yino.ai for normal use and allow localhost only for deliberate local testing.

Risk: Uploaded images or audio are shared with the yino.ai service for generation tasks.

Mitigation: Confirm that source media is appropriate to share with the service before upload.

## Reference(s):

- [Project & Preview Knowledge](artifact/references/project-preview.md)
- [ClawHub Skill Page](https://clawhub.ai/hackerqed/skills/yino-ai)
- [yino.ai API Key Settings](https://yino.ai/settings)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Configuration, Markdown, Guidance]

**Output Format:** [Markdown with inline bash commands, HTTP request examples, JSON examples, and user-facing result links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires YINO_API_KEY; yino.ai generation endpoints return asynchronous task IDs that are polled until output URLs are available.]

## Skill Version(s):

0.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
