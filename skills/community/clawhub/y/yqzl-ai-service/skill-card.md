## Description: <br>
Yqzl Ai Service helps agents submit financial documents for OCR parsing, retrieve asynchronous results, and generate accounting voucher drafts with confidence and review guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hinejon](https://clawhub.ai/user/hinejon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, finance operators, and accounting assistants use this skill to parse bank receipts, bank statements, invoices, and general documents, then summarize results or prepare accounting voucher drafts for human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive financial documents and API credentials through a third-party service, including plain-HTTP service paths. <br>
Mitigation: Install only when the publisher is trusted, avoid sensitive production documents on the plain-HTTP API path, and use non-sensitive test data where possible. <br>
Risk: The skill can silently replace its own code through automatic updates. <br>
Mitigation: Disable or avoid automatic updates unless the update source and release contents can be verified before execution. <br>
Risk: Bundled sample results and generated local preview files may expose financial data. <br>
Mitigation: Review and remove sample result files and generated previews when they contain sensitive or regulated financial information. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hinejon/skills/yqzl-ai-service) <br>
- [Yqzl AI Service Homepage](http://8.135.62.13:5000/) <br>
- [Yqzl AI Experience Page](http://8.135.62.13:5000/AIService/experience/page) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown responses with inline shell commands, JSON result summaries, and paths to generated HTML or JSON preview files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [OCR calls are asynchronous; guidance should avoid resubmitting the same file and may reference generated local previews or accounting voucher JSON.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
