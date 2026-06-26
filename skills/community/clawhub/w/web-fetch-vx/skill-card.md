## Description: <br>
Extracts clean article content and metadata from public or authorized WeChat, news, and blog webpages, with Markdown, JSON, or plain-text output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[3511815125](https://clawhub.ai/user/3511815125) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to extract readable webpage content and title, author, date, and related metadata from authorized public WeChat articles, news pages, and blog posts for summarization, archival, and downstream processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches webpage content over the network and may be misused on private, unauthorized, login-gated, paywalled, or CAPTCHA-protected pages. <br>
Mitigation: Use it only for public or explicitly authorized pages, respect site terms and robots.txt, and avoid access-controlled content. <br>
Risk: Batch processing and caching can increase load on source sites or retain sensitive extracted content. <br>
Mitigation: Limit request volume and concurrency, avoid caching sensitive content, and clear cached data according to retention requirements. <br>
Risk: Custom proxy and User-Agent options can route traffic through untrusted infrastructure or obscure request identity. <br>
Mitigation: Use trusted proxies only and document configured network routing and request identity before deployment. <br>
Risk: Server-resolved provenance is unavailable, and the artifact's OpenClaw Team authorship claim is not independently established by the provided metadata. <br>
Mitigation: Verify publisher identity and source provenance before relying on the skill in sensitive workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/3511815125/web-fetch-vx) <br>
- [OpenClaw Web Content Extractor documentation](https://docs.openclaw.ai/skills/web-content-extractor) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Text, Guidance] <br>
**Output Format:** [Markdown, JSON, or plain text with optional metadata fields.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports batch URL processing and optional title, author, publish date, word count, image, read-time, and extraction-timing metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
