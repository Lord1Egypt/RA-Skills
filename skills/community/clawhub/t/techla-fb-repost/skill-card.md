## Description:

Techla FB Repost helps an agent scrape a Facebook post, rewrite it for a Facebook Page, generate an illustrative image with Gemini, preview the result, and publish through the Facebook Graph API after user confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[techlaai](https://clawhub.ai/user/techlaai)

### License/Terms of Use:


## Use Case:

External users, developers, and social media operators use this skill to turn a supplied Facebook post link into a rewritten Page-ready post with an optional generated image. The workflow supports scraping, rewriting, image generation, preview, confirmation, and publishing to an authorized Facebook Page.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials and Facebook Page access tokens could leak if pasted into chat or command history.

Mitigation: Use protected secrets or environment variables, restrict token scopes, and rotate any token already exposed through examples or command lines.

Risk: The skill can publish content to a Facebook Page.

Mitigation: Use it only with Pages the user owns or is authorized to manage, preview the rewritten text and generated image, and publish only after explicit user confirmation.

Risk: Apify, Google, and Facebook may receive referenced content, prompts, generated images, and final post text.

Mitigation: Confirm that sharing this data with those services is acceptable before processing private or sensitive content.

Risk: The verification flow may request or expose access token values.

Mitigation: Fix the verify command before use so it never requests or prints access_token values.

## Reference(s):

- [API Documentation Reference](references/api_docs.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON results and bash command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Apify, Gemini, and Facebook Page credentials; posting should occur only after user preview and confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
