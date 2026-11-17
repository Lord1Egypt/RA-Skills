## Description:

Turn a blog post URL into a talking-head avatar video where a chosen avatar reads a summarized script against a clean background.

This skill is ready for commercial/non-commercial use.

## Publisher:

[api00](https://clawhub.ai/user/api00)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and developers use this skill to convert a public article URL plus an avatar image or character ID into a narrated talking-head video through the Revid API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Article URLs, avatar image URLs or character IDs, and render metadata are sent to revid.ai under the user's REVID_API_KEY.

Mitigation: Use public or approved content only, avoid private/internal articles or personal images unless third-party processing is accepted, and keep the API key secret.

Risk: Avatar, voice, language, or script-length choices can produce misleading or low-quality talking-head videos.

Mitigation: Set voiceId and language explicitly for the persona, keep target duration concise, and review the generated video before publishing.

Risk: Render polling can fail, delay, or return an error from the third-party API.

Mitigation: Handle failed status responses, retry cautiously, and prefer webhookUrl for production workflows when available.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/api00/skills/revid-blog-to-avatar-video)
- [Revid Render API Endpoint](https://www.revid.ai/api/public/v3/render)
- [Revid Status API Endpoint](https://www.revid.ai/api/public/v3/status?pid=$PID)
- [Revid Consistent Characters API Endpoint](https://www.revid.ai/api/public/v3/consistent-characters)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON payloads, HTTP request templates, bash examples, and a final video URL.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REVID_API_KEY and sends article URL, avatar input, and render metadata to revid.ai.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
