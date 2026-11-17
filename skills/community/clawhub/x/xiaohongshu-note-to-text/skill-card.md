## Description:

Turns Xiaohongshu note and video links into readable text, including captions, image text, transcripts, key points, and optional consumer insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackchew7143](https://clawhub.ai/user/jackchew7143)

### License/Terms of Use:

MIT-0

## Use Case:

External users can provide a Xiaohongshu note link or share text to extract its caption, per-image OCR, video transcript, key points, and engagement details, with optional translation or consumer insights.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: LinkDigest may cache results for public links and share cached results with others requesting the same link; usage history is retained under its privacy policy.

Mitigation: Submit public links only and remove unrelated private text from pasted shares.

Risk: Full outputs and optional analyses can use API credits.

Mitigation: Set --max-credits to cap spending and keep the API key out of conversations.

Risk: The optional MCP bridge adds an external integration dependency.

Mitigation: Pin the optional MCP bridge or skip it.

## Reference(s):

- [LinkDigest documentation](https://linkdigest.dev/zh/docs?ref=skill-xiaohongshu-note-to-text)
- [LinkDigest privacy policy](https://linkdigest.dev/privacy)
- [LinkDigest API specification](https://linkdigest.dev/openapi.json)
- [LinkDigest MCP endpoint](https://linkdigest.dev/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Markdown or JSON with extracted note content and structured fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include per-image OCR and descriptions, video transcript, key points, engagement counts, and optional insights or translation.]

## Skill Version(s):

1.1.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
