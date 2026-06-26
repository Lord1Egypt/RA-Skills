## Description: <br>
Tender Bidding Assistant helps agents analyze tender and RFP documents, draft bid materials, develop bidding strategy, run compliance checks, and plan post-bid follow-up for China government procurement and commercial projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gechengling](https://clawhub.ai/user/gechengling) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Procurement, commercial, and legal reviewers use this skill to analyze bid requirements, prepare tender response materials, review elimination risks, and produce bid strategy guidance. Outputs should be reviewed by qualified procurement or legal staff before submission. <br>

### Deployment Geography for Use: <br>
Global; outputs are tailored primarily to China procurement and tender workflows. <br>

## Known Risks and Mitigations: <br>
Risk: Tender materials can contain confidential prices, client data, identity details, technical secrets, and authorization information. <br>
Mitigation: Redact sensitive data before use, limit file access to project-scoped documents, and process only procurement material the organization permits an AI assistant to handle. <br>
Risk: Generated bid strategy, regulatory claims, and bid documents may be incomplete or incorrect for a specific procurement. <br>
Mitigation: Have qualified procurement or legal staff verify generated documents, compliance claims, and strategy before submission. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gechengling/tender-bidding-assistant) <br>
- [Bid document templates](references/bid-document-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance, bid-document templates, shell commands, Python code, and optional JSON analysis reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read user-provided tender documents and produce checklists, draft bid sections, compliance risk reports, and strategy recommendations.] <br>

## Skill Version(s): <br>
3.2.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
