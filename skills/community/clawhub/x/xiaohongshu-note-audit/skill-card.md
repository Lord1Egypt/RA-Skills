## Description:

Audits social content-marketing note content for policy compliance and shadowban or traffic-throttling risk, including banned words, absolute-claim violations, sensitive content, and compliant rewrite suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wsd-mj](https://clawhub.ai/user/wsd-mj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content teams use this skill to review social note drafts before posting, identify compliance and visibility risks, and receive safer rewrite guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The note text provided for review is sent to ai.wsdsocial.com using the user's WSD_API_KEY.

Mitigation: Avoid submitting confidential drafts, regulated personal data, secrets, or account credentials unless the provider's handling practices are trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wsd-mj/skills/xiaohongshu-note-audit)
- [Server-resolved source provenance](https://github.com/WSD-MJ/xhs-audit/tree/main/xiaohongshu-note-audit)
- [WSD Social API key portal](https://ai.wsdsocial.com/skills)

## Skill Output:

**Output Type(s):** [text, guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with an example curl command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires note content and a WSD_API_KEY for the third-party API.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
