## Description: <br>
This skill takes a Facebook post link, scrapes the post content, rewrites it for a Facebook Page, generates an illustrative image with Gemini, and posts through the Facebook Graph API after user confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[techlaai](https://clawhub.ai/user/techlaai) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External social media operators and page managers use this skill to turn a supplied Facebook link into a rewritten Page-ready post with a generated image, preview it, and publish only after approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Facebook Page posting credentials and access tokens. <br>
Mitigation: Use least-privilege tokens stored in OpenClaw secrets or environment variables, avoid pasting tokens into normal chat or command lines, and avoid the verify command until it stops requesting access_token. <br>
Risk: The workflow sends Facebook links or content to Apify, prompts to Gemini, and final content to Facebook Graph API. <br>
Mitigation: Install only if the publisher is trusted and the operator is comfortable with those external service transfers. <br>
Risk: The skill can publish generated or rewritten content to a live Facebook Page. <br>
Mitigation: Require a visible preview plus explicit approval for the exact Page, post text, and image before publishing. <br>


## Reference(s): <br>
- [API Documentation Reference](references/api_docs.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/techlaai/techla-fb-repost) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API calls, Files, Guidance] <br>
**Output Format:** [Markdown guidance with bash command examples, JSON script outputs, rewritten Facebook post text, a generated image file, and a final Facebook post link when publishing succeeds.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Apify, Gemini, and Facebook Page credentials; the workflow calls for preview and explicit user approval before publishing.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
