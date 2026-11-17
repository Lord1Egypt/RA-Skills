## Description:

Generates and optimizes professional B2B LinkedIn outreach messages, connection requests, and follow-up sequences from user-provided prospect and campaign context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangm-a3](https://clawhub.ai/user/wangm-a3)

### License/Terms of Use:

MIT-0

## Use Case:

Sales, business development, and customer-development users use this skill to draft personalized B2B LinkedIn outreach, improve message quality, and plan multi-step follow-up sequences. The skill is intended for human-reviewed copy-paste sending rather than automated social-platform access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prospect or customer details may be sent to an external Yunlv AI API when external generation is used.

Mitigation: Use only with an appropriate consent or legal basis, avoid unnecessary identifiers, and minimize names, profile URLs, employers, titles, and notes before generation.

Risk: The artifact makes conflicting privacy and retention claims for customer or prospect information.

Mitigation: Do not rely on retention, deletion, or non-storage statements unless the publisher provides enforceable terms that cover the intended use.

Risk: Generated outreach may be inaccurate, misleading, or unsuitable for platform rules.

Mitigation: Require human review for personalization accuracy, claims, tone, message limits, and social-platform compliance before sending.

## Reference(s):

- [Yunlv Homepage](https://yunlvai.com)
- [Yunlv AI MatchGPT API](https://api.yunlvai.com)
- [LinkedIn Message Templates](references/linkedin_message_templates.md)
- [Industry Hooks Library](references/industry_hooks_library.md)
- [Follow-up Sequence Templates](references/followup_sequence_templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and message drafts, with optional JSON output from the included command-line optimizer.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use TRADEGPT_API_KEY for external Yunlv AI generation; generated outreach should be reviewed before use.]

## Skill Version(s):

1.1.0 (source: release evidence and clawhub.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
