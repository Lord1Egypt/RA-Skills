## Description:

Turn any news article or long-form post URL into a 30-60 second 9:16 short with stock visuals, narration, and captions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[api00](https://clawhub.ai/user/api00)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content teams use this skill to turn article URLs into edited vertical summary videos through Revid. It is suited to public news articles, long-form posts, press releases, and essays where the desired result is narration, stock visuals, captions, and a returned video URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Article URLs are sent to Revid for rendering.

Mitigation: Do not use internal, private, paywalled, or sensitive links unless that sharing is acceptable for the deployment environment.

Risk: The skill requires a Revid API key.

Mitigation: Keep REVID_API_KEY scoped to Revid, store it in configuration rather than skill text, and rotate it if exposed.

## Reference(s):

- [Article to Short ClawHub page](https://clawhub.ai/api00/skills/revid-article-to-short)
- [Revid render endpoint](https://www.revid.ai/api/public/v3/render)
- [Revid status endpoint](https://www.revid.ai/api/public/v3/status?pid=$PID)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON and bash examples, ending with a video URL when rendering succeeds]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REVID_API_KEY and sends the supplied article URL to Revid.]

## Skill Version(s):

1.3.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
