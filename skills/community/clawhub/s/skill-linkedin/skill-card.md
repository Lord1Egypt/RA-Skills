## Description: <br>
Generates personalized LinkedIn connection requests, outreach messages, and follow-up sequences for B2B prospecting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangm-a3](https://clawhub.ai/user/wangm-a3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sales and business-development users use this skill to draft tailored LinkedIn connection requests, prospect messages, and follow-up sequences from provided prospect or profile context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive LinkedIn credentials or session tokens may grant account authority. <br>
Mitigation: Prefer OAuth and draft-only or manual sending, avoid raw session tokens where possible, protect stored credentials, and revoke access when no longer needed. <br>
Risk: Automated outreach and batch sending may violate platform rules or produce unwanted spam. <br>
Mitigation: Review every message before sending, keep batches small, respect LinkedIn limits, and use manual approval for outbound messages. <br>
Risk: Prospect profiles, generated messages, sent records, and logs may be stored locally without clear retention controls. <br>
Mitigation: Store only necessary data, restrict local access, define retention and deletion practices, and confirm records can be removed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wangm-a3/skill-linkedin) <br>
- [Publisher Profile](https://clawhub.ai/user/wangm-a3) <br>
- [Yunlv AI Homepage](https://yunlvai.com) <br>
- [Yunlv AI MatchGPT API](https://api.yunlvai.com) <br>
- [LinkedIn API](https://api.linkedin.com) <br>
- [LinkedIn Message Templates](references/linkedin_message_templates.md) <br>
- [Industry Hooks Library](references/industry_hooks_library.md) <br>
- [Follow-up Sequence Templates](references/followup_sequence_templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown text with message drafts, follow-up sequence tables, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include multiple message variants, timing steps, and manual review guidance.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter 1.0.0 and clawhub.yaml 1.0.2 differ) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
