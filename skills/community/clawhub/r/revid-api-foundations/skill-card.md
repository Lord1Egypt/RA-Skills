## Description: <br>
Foundation knowledge for Revid skills covering authentication, the render endpoint, workflow selection, polling, webhooks, and the response envelope. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[api00](https://clawhub.ai/user/api00) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill as foundational guidance for calling the Revid Public API v3, including authentication, request shape, workflow selection, status polling, webhooks, and common failure handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Revid API key and sends video-generation inputs to Revid.ai. <br>
Mitigation: Use a scoped or dedicated API key where possible, avoid sharing confidential prompts, scripts, URLs, or secrets, and rotate the key if exposure is suspected. <br>
Risk: Webhook URLs can expose generated job data or send callbacks to an unintended endpoint. <br>
Mitigation: Use webhooks only with a trusted public endpoint; otherwise prefer polling the status endpoint. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/api00/revid-api-foundations) <br>
- [api00 publisher profile](https://clawhub.ai/user/api00) <br>
- [Revid Public API v3 spec](https://documenter.getpostman.com/view/36975521/2sBXcGEfaB) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with API examples, JSON snippets, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REVID_API_KEY for API calls; guidance covers polling and optional webhook use.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
