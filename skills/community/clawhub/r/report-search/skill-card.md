## Description: <br>
Searches and retrieves research reports from fxbaogao.com, including industry reports, company research, macro strategy reports, financial reports, and prospectuses, with filters for keyword, organization, author, and time range. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EliaukTM](https://clawhub.ai/user/EliaukTM) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to search fxbaogao.com research reports, review result metadata, and retrieve summaries or selected report content by document ID. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms, author or organization filters, and selected document IDs are sent to fxbaogao.com. <br>
Mitigation: Install only if this external service use is acceptable for the intended workflow and data handling requirements. <br>
Risk: SSL verification can be disabled with FXBAOGAO_SSL_NO_VERIFY=1. <br>
Mitigation: Keep SSL verification enabled by default and use the bypass only briefly for a known local certificate-chain problem. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/EliaukTM/report-search) <br>
- [fxbaogao report site](https://www.fxbaogao.com) <br>
- [fxbaogao API service](https://api.fxbaogao.com) <br>
- [Usage examples](examples/sample.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON from local scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results include report metadata such as doc_id, organization, author, date, links, snippets, and optional detail summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
