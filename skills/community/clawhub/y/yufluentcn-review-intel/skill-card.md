## Description:

Analyzes user-provided cross-border ecommerce reviews to cluster sentiment themes, identify complaint causes, and produce structured improvement suggestions and reply-template drafts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[metahuan](https://clawhub.ai/user/metahuan)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers and ecommerce operators use this skill to analyze legally obtained Amazon, Shopify, or TikTok Shop review text for sentiment themes, complaint causes, prioritized improvements, and draft customer replies. Agents can use it to normalize review inputs, run the packaged CLI or API flow, and explain the resulting JSON insights.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Review contents and the TOKENAPI_KEY account credential can be sent to a configured endpoint, including an arbitrary TOKENAPI_BASE_URL.

Mitigation: Use only a trusted HTTPS endpoint or trusted local proxy, avoid submitting buyer PII or confidential business data unless policy allows cloud processing, and rotate the token if it may have been used with an untrusted endpoint.

Risk: Generated complaint themes, improvement suggestions, and reply templates may be inaccurate or unsuitable for customer-facing use.

Mitigation: Review the structured analysis and all reply drafts before making product decisions or sending messages to buyers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/metahuan/skills/yufluentcn-review-intel)
- [Yufluent OpenClaw app](https://claw.changzhiai.com/app/openclaw)
- [Yufluent homepage](https://claw.changzhiai.com)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Structured JSON insights with optional Markdown explanations and CLI command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TOKENAPI_KEY; accepts review text or a UTF-8 reviews file plus optional product, platform, and language settings.]

## Skill Version(s):

1.1.2 (source: server release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
