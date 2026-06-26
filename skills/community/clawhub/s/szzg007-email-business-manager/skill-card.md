## Description: <br>
Manages cross-border ecommerce mailboxes across business lines by classifying customer emails, extracting communication history, and generating multilingual reply suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[szzg007](https://clawhub.ai/user/szzg007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cross-border ecommerce operators use this skill to organize customer mail by product line, retrieve prior communication context, and prepare professional multilingual replies for sales, support, and B2B follow-up workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to access business mailbox credentials and customer email history. <br>
Mitigation: Use app-specific or least-privilege mailbox credentials and require confirmation before reading real customer histories or mailbox content. <br>
Risk: Generated replies or CRM sync actions may affect customer communications and records. <br>
Mitigation: Review draft replies and customer-data sync proposals before sending, storing, or updating production records. <br>
Risk: Local storage of emails and customer records can create retention and deletion obligations. <br>
Mitigation: Define approved storage locations, retention periods, access controls, and deletion procedures before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/szzg007/szzg007-email-business-manager) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown reports, email reply drafts, structured configuration examples, and guidance text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include customer communication timelines, classification labels, business-line filters, and draft email responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
