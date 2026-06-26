## Description: <br>
Generates personalized LinkedIn connection requests, outreach messages, and follow-up sequences for B2B lead generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangm-a3](https://clawhub.ai/user/wangm-a3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sales and business development users use this skill to draft personalized LinkedIn outreach, connection requests, message variants, and multi-step follow-up sequences for prospective B2B customers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for a sensitive LinkedIn session token and does not clearly bound how account access is used. <br>
Mitigation: Install only if the publisher is trusted with LinkedIn session access and token handling, retention, and no-logging behavior are documented. <br>
Risk: LinkedIn outreach can create account-policy and privacy exposure if messages are sent without review or if account data is mishandled. <br>
Mitigation: Review generated outreach before sending and avoid providing a session token unless the workflow requires explicit review before any outreach is sent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangm-a3/yunlv-linkedin-outreach) <br>
- [Yunlv AI homepage](https://yunlvai.com) <br>
- [Yunlv AI MatchGPT API](https://api.yunlvai.com) <br>
- [LinkedIn message templates](references/linkedin_message_templates.md) <br>
- [Industry hooks library](references/industry_hooks_library.md) <br>
- [Follow-up sequence templates](references/followup_sequence_templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Configuration] <br>
**Output Format:** [Markdown with generated outreach copy, tables, templates, and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use TRADEGPT_API_KEY and LinkedIn session credentials when configured; generated LinkedIn messages are intended for user review and manual copying or third-party sending.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
