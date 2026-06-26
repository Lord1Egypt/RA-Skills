## Description: <br>
Use this skill when the user wants to manage social media scheduling, analytics, cross-posting, or AI-assisted content creation across Instagram, TikTok, Twitter/X, LinkedIn, or Facebook. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[saintlittlefish](https://clawhub.ai/user/saintlittlefish) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, social media managers, and developers use this skill to plan posts, adapt content across major social platforms, generate approved replies, and summarize social performance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package includes preconfigured SkillPay billing code with an exposed API key and a charge function. <br>
Mitigation: Remove or disable the bundled SkillPay files unless monetization is intended, rotate the exposed key if it is real, and require clear user confirmation before any billing call. <br>
Risk: Social platform tokens and queued drafts may expose account access, unpublished content, or brand-sensitive information. <br>
Mitigation: Use least-privilege platform tokens, store queued drafts only in a private project directory, and avoid committing local queue files or credentials. <br>
Risk: Generated posts, cross-post adaptations, and replies may be inaccurate, off-brand, or inappropriate for a platform context. <br>
Mitigation: Require human approval before publishing posts or sending replies, and check generated content against brand guidelines and platform rules. <br>


## Reference(s): <br>
- [Platform Specifications](references/platform-specs.md) <br>
- [Caption Templates](assets/templates/captions.md) <br>
- [ClawHub skill page](https://clawhub.ai/saintlittlefish/xanadu-social-manager) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown, Python code snippets, configuration guidance, queued post records, and analytics report text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided social platform tokens and optional SkillPay configuration; posting, replies, and billing should require explicit user approval.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
