## Description: <br>
China Telecom account managers can enter an enterprise name to search public company information, identify business opportunities, generate visit scripts, and produce a visit preparation report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[keyangwang0726](https://clawhub.ai/user/keyangwang0726) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
China Telecom enterprise account managers use this skill to prepare for customer visits by collecting public enterprise information, matching China Telecom products to likely needs, drafting visit plans and scripts, and generating a structured preparation report. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may require sensitive search or MCP credentials. <br>
Mitigation: Use trusted search or MCP providers and scope API keys to the minimum access needed. <br>
Risk: Users may enter confidential non-public customer details while preparing a report. <br>
Mitigation: Avoid entering confidential customer information unless the execution environment and data handling rules are approved for that data. <br>
Risk: Generated enterprise facts and opportunity recommendations may be outdated, incomplete, or inaccurate. <br>
Mitigation: Verify generated facts and recommendations against current sources before sharing or using them in customer conversations. <br>
Risk: Optional Word document export writes a report file that may contain customer information. <br>
Mitigation: Export .docx reports only when needed, save them in an approved location, and handle the files according to customer-data retention rules. <br>
Risk: Adding the skill to persistent project instructions can keep sales workflow guidance active beyond a single task. <br>
Mitigation: Add the skill to persistent instructions only for workspaces where this visit-prep behavior is intended. <br>


## Reference(s): <br>
- [Telecom product knowledge base](artifact/references/telecom-products.md) <br>
- [Visit speech script templates](artifact/references/speech-scripts.md) <br>
- [Visit report template](artifact/references/report-template.md) <br>
- [ClawHub skill page](https://clawhub.ai/keyangwang0726/telecom-visit-prep) <br>
- [Project homepage](https://github.com/KeyangWang0726/telecom-visit-prep) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands, configuration, files] <br>
**Output Format:** [Conversational Markdown report with optional Word document export] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask whether to export a .docx report after presenting the Markdown report.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
