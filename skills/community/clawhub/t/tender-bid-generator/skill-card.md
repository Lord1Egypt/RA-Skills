## Description: <br>
Generate bid proposal drafts from tender documents by extracting requirements, structuring response sections, and preparing Word-compatible bid content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chengcheng8632](https://clawhub.ai/user/chengcheng8632) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and business proposal teams use this skill to parse PDF, Word, or text tender documents and draft compliant bid materials for human review before submission. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tender documents may contain sensitive commercial, pricing, or qualification information. <br>
Mitigation: Let the agent read only the specific tender files provided for the task and keep generated bid drafts in a controlled location. <br>
Risk: Generated bid drafts may contain incorrect pricing, compliance claims, qualification statements, or technical responses. <br>
Mitigation: Have a qualified person review all pricing, compliance, qualification, and technical content before submission. <br>
Risk: Parsing or template generation depends on local document-processing packages and user-selected file paths. <br>
Mitigation: Confirm the exact file path before parsing and install dependencies only from trusted sources. <br>


## Reference(s): <br>
- [Writing Guide](references/writing-guide.md) <br>
- [Bid Template](assets/bid-template.txt) <br>
- [ClawHub Skill Page](https://clawhub.ai/chengcheng8632/tender-bid-generator) <br>
- [Publisher Profile](https://clawhub.ai/user/chengcheng8632) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown and text bid drafts with JSON extraction output and optional Word-compatible document files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated bid content requires human review for pricing, compliance, qualification evidence, and submission readiness.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
