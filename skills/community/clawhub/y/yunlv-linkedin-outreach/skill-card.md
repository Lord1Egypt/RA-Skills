## Description:

Generates personalized LinkedIn connection requests, outreach messages, and follow-up sequences for B2B lead generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangm-a3](https://clawhub.ai/user/wangm-a3)

### License/Terms of Use:

MIT-0

## Use Case:

External sales, marketing, and business development users use this skill to draft LinkedIn outreach, personalize message hooks from prospect context, and plan multi-step follow-up sequences. The skill supports user-driven copying or third-party sending workflows rather than direct LinkedIn message sending.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill metadata requests LINKEDIN_SESSION_TOKEN even though the documented workflow is message drafting and manual or third-party sending.

Mitigation: Use the skill as a drafting aid only and do not provide a LinkedIn session token unless the publisher documents its scope, storage, revocation, and transmission behavior.

Risk: Generated outreach can become spammy, misleading, or policy-sensitive if sent in bulk without review.

Mitigation: Review each generated message for accuracy, personalization, consent expectations, and platform policy fit before sending.

## Reference(s):

- [Skill Linkedin ClawHub Release](https://clawhub.ai/wangm-a3/skills/yunlv-linkedin-outreach)
- [Yunlv AI Homepage](https://yunlvai.com)
- [Yunlv AI MatchGPT API](https://api.yunlvai.com)
- [LinkedIn Message Templates](references/linkedin_message_templates.md)
- [Industry Hooks Library](references/industry_hooks_library.md)
- [Follow-up Sequence Templates](references/followup_sequence_templates.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration]

**Output Format:** [Markdown prose, message templates, follow-up sequences, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use TRADEGPT_API_KEY for Yunlv AI MatchGPT content generation; artifact metadata also lists LINKEDIN_SESSION_TOKEN.]

## Skill Version(s):

1.0.4 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
