## Description:

OpenClaw AI agent skill for automated TikTok and Instagram carousel growth that analyzes a website URL, extracts brand and positioning details, generates carousel slides, publishes through Upload-Post, and uses analytics feedback for later posts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mutonby](https://clawhub.ai/user/mutonby)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and developers use Viraloop to turn a public website into a six-slide TikTok and Instagram carousel, publish it through Upload-Post, and use analytics feedback to improve later posts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish generated content directly to public TikTok and Instagram feeds.

Mitigation: Use dedicated low-privilege Upload-Post tokens and require human review or a dry-run gate before running the publish step.

Risk: The documented autonomous loop may alter posting schedules based on analytics without explicit operator approval.

Mitigation: Keep schedule changes outside the skill's automatic execution path and review any cron or automation updates before applying them.

Risk: Website analysis accepts arbitrary public URLs and sends derived prompts to external image-generation services.

Mitigation: Analyze only public sites the operator trusts or controls, and avoid entering private, authenticated, or sensitive URLs.

Risk: The bundled publisher script builds a curl command string and executes it with eval.

Mitigation: Treat captions, usernames, and generated metadata as untrusted input and inspect the publish command path before use.

## Reference(s):

- [Viraloop ClawHub listing](https://clawhub.ai/mutonby/skills/viraloop)
- [Upload-Post photo upload API](https://docs.upload-post.com/api/upload-photo)
- [Upload-Post analytics API](https://docs.upload-post.com/api/get-analytics)
- [Google AI Studio API keys](https://aistudio.google.com/app/apikey)
- [Upload-Post](https://upload-post.com)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown instructions with shell commands, generated JSON, JPG carousel images, captions, and local analytics files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local files under /tmp/carousel and may publish public TikTok and Instagram posts when configured with Upload-Post credentials.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
