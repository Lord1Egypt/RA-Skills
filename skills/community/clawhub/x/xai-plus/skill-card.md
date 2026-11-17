## Description:

Search X/Twitter and the web, chat with Grok models using text or images, and analyze X content using xAI's API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mischasigtermans](https://clawhub.ai/user/mischasigtermans)

### License/Terms of Use:


## Use Case:

Developers, researchers, and content teams use this skill to search X and the web through Grok, chat with xAI models, analyze images, and review X content patterns or draft-post quality.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, queries, images or screenshots, draft posts, X URLs, and public account analysis targets may be sent to xAI.

Mitigation: Use only with data approved for xAI processing, and avoid submitting confidential, regulated, or sensitive material unless the deployment has appropriate authorization.

Risk: The skill can read an xAI API key from environment variables or local Clawdbot configuration, including fallback skill entries.

Mitigation: Review local credential configuration before use, scope keys to the intended account, and rotate keys if they may have been exposed.

Risk: Voice analysis and post-optimization workflows could be misused for impersonation, deceptive content, spam, or evading platform safeguards.

Mitigation: Use these workflows only for legitimate analysis and quality review, and do not use them to impersonate people, automate deceptive engagement, produce spam, or bypass platform rules.

## Reference(s):

- [xAI Plus ClawHub Skill Page](https://clawhub.ai/mischasigtermans/skills/xai-plus)
- [xAI API Console](https://console.x.ai)
- [xAI API Reference](references/api-reference.md)
- [xAI Models Reference](references/models.md)
- [Search Patterns and Optimization](references/search-patterns.md)
- [Analysis Prompts Reference](references/analysis-prompts.md)
- [X Algorithm Reference](references/x-algorithm.md)
- [xAI API Base URL](https://api.x.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and optional JSON or plain-text command output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and an XAI_API_KEY; command outputs may include xAI-generated citations, X URLs, model lists, analysis scores, or image-analysis responses.]

## Skill Version(s):

2.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
