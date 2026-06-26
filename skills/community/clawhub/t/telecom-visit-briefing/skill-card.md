## Description: <br>
Generate professional client visit briefings and follow-up action plans from visit records, meeting notes, handwritten notes, or chat logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[keyangwang0726](https://clawhub.ai/user/keyangwang0726) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Telecom enterprise account managers use this skill to turn customer visit records, meeting notes, handwritten notes, and chat logs into structured visit briefings, opportunity analysis, follow-up plans, and sales scripts. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: Generated briefings and follow-up plans may contain confidential customer visit details, business opportunities, pricing, or security-related information. <br>
Mitigation: Install and use only when authorized to process the provided customer records; treat generated reports and exported Word files as confidential business documents. <br>
Risk: Generated recommendations or scripts may be incomplete or unsuitable for sharing without account-manager review. <br>
Mitigation: Review each briefing, follow-up plan, recommendation, and sales script before sending it to customers or internal stakeholders. <br>
Risk: Optional Word export depends on a separately installed docx tool. <br>
Mitigation: Verify any docx skill or dependency from a trusted source before installation and continue using chat-based Markdown output when export support is unavailable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/keyangwang0726/telecom-visit-briefing) <br>
- [README](artifact/README.md) <br>
- [Briefing template](artifact/references/briefing-template.md) <br>
- [Follow-up template](artifact/references/followup-template.md) <br>
- [Telecom product knowledge base](artifact/references/telecom-products.md) <br>
- [Sales script templates](artifact/references/speech-scripts.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, files] <br>
**Output Format:** [Markdown reports in chat, with optional Word document export after user confirmation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May process text records, chat logs, and OCR text from handwritten notes; Word export requires a separately installed docx skill.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
