## Description: <br>
QA pass to catch and fix AI-pattern tells in tweets before publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nissan](https://clawhub.ai/user/nissan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Social media editors, developers, and agents use this skill to audit existing tweets or short-form posts for AI-pattern tells and rewrite flagged text while preserving the author's voice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Duplicate metadata and inconsistent Ollama/network declarations can confuse install-time permission expectations. <br>
Mitigation: Confirm whether local Ollama access is required before deployment and retain one clear permission declaration. <br>
Risk: Automated tweet rewrites can change tone, meaning, or intended emphasis before publication. <br>
Mitigation: Review the flagged patterns and humanized text before posting or scheduling. <br>


## Reference(s): <br>
- [Tweet Humanizer on ClawHub](https://clawhub.ai/nissan/tweet-humanizer) <br>
- [nissan publisher profile](https://clawhub.ai/user/nissan) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with original tweet, detected flags, humanized rewrite, and character count.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Rewrites are constrained to tweet-length short-form posts and should preserve requested hashtags.] <br>

## Skill Version(s): <br>
1.0.3 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
