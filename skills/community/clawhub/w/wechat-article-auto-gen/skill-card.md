## Description: <br>
Automates WeChat article production by rewriting reference content, creating storyboards and image prompts, generating cover guidance, and assembling WeChat-ready HTML. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dally-bee](https://clawhub.ai/user/dally-bee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing operators and content creators use this skill to transform reference WeChat articles into MUX-branded fitness content with article text, storyboard sections, image prompts, cover design guidance, and HTML output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A hardcoded image-provider API key is exposed in the skill material. <br>
Mitigation: Do not use the embedded credential; replace it with a scoped key managed outside the skill before installation or execution. <br>
Risk: Scraped or rewritten articles may include content the user does not have rights to process. <br>
Mitigation: Only process articles the user is authorized to scrape, rewrite, and republish, and review the final content for rights and platform compliance. <br>
Risk: Article content may be sent to external AI or image-generation services. <br>
Mitigation: Avoid confidential material and confirm destination URLs, model providers, and data-sharing terms before sending source content to external services. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dally-bee/wechat-article-auto-gen) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python and HTML examples, generated article text, image prompts, cover specifications, and HTML output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may depend on external article sources, LLM providers, and image-generation services; generated content should be reviewed before publication.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
