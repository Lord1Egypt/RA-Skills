## Description: <br>
Zoho Bigin API integration with managed OAuth for managing contacts, companies, pipelines, and products in Bigin CRM. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and CRM operators use this skill to read, search, create, update, and delete Zoho Bigin CRM records through Maton-managed OAuth. It is intended for workflows involving contacts, companies, sales pipelines, products, connection management, and CRM metadata lookup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A leaked or mishandled MATON_API_KEY could expose Zoho Bigin data through Maton's proxy. <br>
Mitigation: Keep MATON_API_KEY private, avoid printing it in logs, and rotate it if exposure is suspected. <br>
Risk: Create, update, delete, and OAuth connection deletion requests can change real CRM data or access paths. <br>
Mitigation: Require explicit user approval before executing any write or deletion operation, including confirmation of the target resource and intended effect. <br>
Risk: When multiple Zoho Bigin connections exist, requests may target the wrong account. <br>
Mitigation: Confirm the intended connection and include the Maton-Connection header when more than one connection is available. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/byungkyu/zoho-bigin) <br>
- [Publisher profile](https://clawhub.ai/user/byungkyu) <br>
- [Bigin API Overview](https://www.bigin.com/developer/docs/apis/v2/) <br>
- [Bigin REST API Documentation](https://www.bigin.com/developer/docs/apis/) <br>
- [Modules API](https://www.bigin.com/developer/docs/apis/modules-api.html) <br>
- [Maton](https://maton.ai) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with Python and JavaScript code examples, shell snippets, HTTP endpoint references, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MATON_API_KEY and network access; generated requests may read or modify Zoho Bigin CRM records.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
