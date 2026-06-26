## Description: <br>
Zero-trust email triage prioritizes inbox messages by sender trust tier, surfaces customer and active-contact emails, batches newsletters and notifications, and treats unknown-sender urgency claims cautiously. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stevenobiajulu](https://clawhub.ai/user/stevenobiajulu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People using an email-capable agent use this skill to triage unread inboxes by sender trust, identify priority customer or active-contact messages, and batch lower-priority notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad triage activation can expose email metadata and limited previews to the agent. <br>
Mitigation: Install only where that access is acceptable, use explicit prompts such as "triage my inbox", and confirm whether connected CRM or customer-directory data should be used. <br>
Risk: Sender-priority rules can misclassify unknown but important messages. <br>
Mitigation: Review the priority sender list and exception-lane elevations before acting on triage results. <br>


## Reference(s): <br>
- [Homepage](https://github.com/UseJunior/email-agent-mcp) <br>
- [ClawHub skill page](https://clawhub.ai/stevenobiajulu/zero-trust-email-triage) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown triage summaries with grouped priority lists and action flags] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; relies on email data already available to the agent runtime and does not request credentials.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
