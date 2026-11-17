## Description:

Generates images through the Wuyin Keji API using NanaBanana 2 by default and NanaBanana Pro for high-quality, realistic, or final artwork.

This skill is ready for commercial/non-commercial use.

## Publisher:

[riage](https://clawhub.ai/user/riage)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit English image prompts, select model quality, size, and aspect ratio, poll for completion, and return generated image URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API key exposure in URL query parameters during result polling.

Mitigation: Use a limited, revocable API key, avoid sensitive prompts, prefer header-based polling when available, and rotate any key already used in query strings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/riage/skills/skill-paintinginterface)
- [Wuyin Keji API service](https://api.wuyinkeji.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Guidance]

**Output Format:** [Markdown/text response with <qqimg> image URL tags and model, ratio, and resolution details.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Polls every 3 seconds up to 20 attempts; prompts should be translated to detailed English before submission.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
