## Description:

Turn an X/Twitter/LinkedIn post (URL or pasted thread text) into a talking-head video that delivers the take.

This skill is ready for commercial/non-commercial use.

## Publisher:

[api00](https://clawhub.ai/user/api00)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and agents use this skill to repurpose an X/Twitter thread, LinkedIn post, or pasted post text into a short talking-head video with avatar, voiceover, captions, and light motion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Post text, source URLs, avatar image URLs, and the Revid API key are sent to a third-party service.

Mitigation: Avoid private or confidential content and review Revid's data handling terms before use.

Risk: The example status request follows redirects while sending the API key.

Mitigation: Fix or avoid the redirect-following status request unless the API-key exposure risk is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/api00/skills/revid-tweet-to-talking-head)
- [Revid render API endpoint](https://www.revid.ai/api/public/v3/render)

## Skill Output:

**Output Type(s):** [guidance, configuration, JSON, shell commands]

**Output Format:** [Markdown guidance with JSON API payloads and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REVID_API_KEY and sends post text or URLs plus avatar image URLs to Revid.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
