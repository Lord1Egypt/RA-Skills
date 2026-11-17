## Description:

Turns supported video links into spoken transcripts, on-screen text, summaries, translations, and engagement metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackchew7143](https://clawhub.ai/user/jackchew7143)

### License/Terms of Use:

MIT-0

## Use Case:

People reviewing public video links use this skill to extract spoken content, on-screen text, summaries, translations, and engagement statistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Supplied links or share text are uploaded for processing; results may be cached and shared with users requesting the same link, and third-party providers process the content.

Mitigation: Submit public links, remove unrelated personal information from share text, and review the LinkDigest privacy policy.

Risk: Full transcripts and optional processing can consume credits, and the API key authorizes usage.

Mitigation: Keep LINKDIGEST_API_KEY private and set --max-credits or a key spending limit.

Risk: The optional MCP bridge adds a third-party dependency.

Mitigation: Prefer the bundled Python client or pin a reviewed version when using the MCP bridge.

## Reference(s):

- [LinkDigest documentation](https://linkdigest.dev/zh/docs?ref=skill-tiktok-transcript)
- [LinkDigest privacy policy](https://linkdigest.dev/privacy)
- [LinkDigest OpenAPI specification](https://linkdigest.dev/openapi.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Markdown or JSON digest with transcript text, timestamps, on-screen text, summaries, and video metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional translation; transcript timestamps are segment-level and on-screen timestamps are approximate.]

## Skill Version(s):

1.0.3 (source: frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
