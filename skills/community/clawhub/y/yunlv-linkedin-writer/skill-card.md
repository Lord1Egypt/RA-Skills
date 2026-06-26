## Description: <br>
Generates professional B2B outreach messages, LinkedIn-style connection requests, and follow-up sequences from user-provided prospect and company context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangm-a3](https://clawhub.ai/user/wangm-a3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sales, export, and customer-development users use this skill to draft personalized B2B outreach messages, optimize short social connection requests, and plan multi-step follow-up sequences for prospects. It produces draft content for human review and manual sending. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prospect and company context may be sent to Yunlv's API with the user's TRADEGPT_API_KEY. <br>
Mitigation: Enter only the minimum context needed for drafting, and avoid confidential notes, regulated personal data, sensitive business context, or unnecessary LinkedIn profile URLs. <br>
Risk: Generated outreach messages may contain inaccurate, misleading, or non-compliant claims. <br>
Mitigation: Review and edit every message before sending, verify personalization details, and keep manual control of any social platform interaction. <br>
Risk: Generated messages and sequences may remain in the local data directory. <br>
Mitigation: Clear ./data/yunlv-skills/linkedinWriter/ when generated content contains information that should not be retained. <br>


## Reference(s): <br>
- [LinkedIn Message Templates](references/linkedin_message_templates.md) <br>
- [Industry Hooks Library](references/industry_hooks_library.md) <br>
- [Follow-up Sequence Templates](references/followup_sequence_templates.md) <br>
- [Yunlv Homepage](https://yunlvai.com) <br>
- [Yunlv MatchGPT API](https://api.yunlvai.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/wangm-a3/yunlv-linkedin-writer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands] <br>
**Output Format:** [Markdown prose, message drafts, follow-up tables, and JSON from the bundled optimizer script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated outreach should be reviewed by a human before use; the optimizer script prints JSON to stdout.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and clawhub.yaml; SKILL.md frontmatter lists 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
