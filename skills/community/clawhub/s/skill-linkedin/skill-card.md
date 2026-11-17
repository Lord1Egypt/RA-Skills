## Description:

Generates personalized LinkedIn connection requests, outreach messages, and follow-up sequences for B2B prospects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangm-a3](https://clawhub.ai/user/wangm-a3)

### License/Terms of Use:

MIT-0

## Use Case:

External sales, customer-development, and B2B outreach users use this skill to draft LinkedIn connection requests, personalized prospect messages, and multi-step follow-up sequences. It is intended for user-reviewed outreach and can support manual sending or authorized LinkedIn message sending.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can involve a raw LinkedIn session token and account-level message sending behavior.

Mitigation: Prefer OAuth with explicit consent, avoid sharing raw session tokens with untrusted runtimes, and require user confirmation before any automatic LinkedIn sends.

Risk: Imported profiles, generated messages, sent records, and logs may be stored locally.

Mitigation: Review local storage paths and retention practices before installation, and keep prospect data limited to what the user is authorized to process.

Risk: Automated or repetitive LinkedIn outreach can create compliance, account, or spam-risk issues.

Mitigation: Keep message generation separate from sending, review messages before use, personalize outreach, and respect LinkedIn limits and policies.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wangm-a3/skills/skill-linkedin)
- [Yunlv AI Homepage](https://yunlvai.com)
- [Yunlv AI MatchGPT API](https://api.yunlvai.com)
- [LinkedIn API](https://api.linkedin.com)
- [LinkedIn Message Templates](references/linkedin_message_templates.md)
- [Industry Hooks Library](references/industry_hooks_library.md)
- [Follow-up Sequence Templates](references/followup_sequence_templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown or plain text outreach drafts, message variants, and follow-up sequence tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include personalized connection requests, private messages, A/B variants, character-limit checks, and multi-step follow-up timing.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
