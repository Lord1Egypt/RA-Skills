## Description: <br>
Generate social media content (posts, captions, images) for multiple platforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinanping-CPU](https://clawhub.ai/user/yinanping-CPU) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Marketing, social media, and developer users use this skill to draft platform-optimized posts, captions, image prompts, and content calendar assets for Twitter/X, Instagram, LinkedIn, and Facebook. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AI mode sends post topics and image prompts to OpenAI. <br>
Mitigation: Use --no-ai for local template-only generation when needed, and avoid entering confidential campaign or client information. <br>
Risk: Optional publishing workflows require social-platform API credentials. <br>
Mitigation: Keep .env files and API tokens out of source control, and do not provide platform tokens or run upload workflows unless the uploader code has been separately reviewed. <br>
Risk: Generated social content may be inaccurate, off-brand, or unsuitable for publication without review. <br>
Mitigation: Review generated posts, captions, metadata, and images before publishing or scheduling them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yinanping-CPU/yinan-social-content-generator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples; generated artifacts include post.txt, metadata.json, and optional PNG images.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports AI-backed generation through OpenAI when configured, with a template-only fallback via --no-ai.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
