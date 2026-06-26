## Description: <br>
Automates quotation generation in Excel, Word, HTML, and PDF formats with data validation to reduce example-data misuse and optional OKKI CRM support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cjboy007](https://clawhub.ai/user/cjboy007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales and operations agents use this skill to create customer-specific quotation files, validate quotation data before generation, and prepare PDF attachments for outbound customer workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Quotation data may be passed to an external OKKI sync workflow. <br>
Mitigation: Review and control whether OKKI synchronization runs before using the generated workflow with customer data. <br>
Risk: Generated quotations may contain sensitive customer or commercial details. <br>
Mitigation: Review generated files before sending, avoid online PDF tools, and use an explicit recipient and attachment confirmation process. <br>
Risk: Generated HTML loads assets from public CDNs. <br>
Mitigation: Replace CDN-loaded HTML assets with local copies when operating in restricted or sensitive environments. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cjboy007/quotation-workflow) <br>
- [Skill Instructions](SKILL.md) <br>
- [Quick Start](QUICK_START.md) <br>
- [Workflow Checklist](WORKFLOW_CHECKLIST.md) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with JSON data templates, shell commands, and generated quotation files such as HTML and PDF.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3 and Chrome; server metadata lists macOS compatibility.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
