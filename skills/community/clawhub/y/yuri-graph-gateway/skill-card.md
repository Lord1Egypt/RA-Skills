## Description: <br>
Yuri Graph Gateway is a usage guide for routing Facebook Graph API requests through the baiz.ai proxy by replacing the Facebook Graph domain and using a Yuri API token. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuriskills](https://clawhub.ai/user/yuriskills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and API integrators use this skill to adapt existing Facebook Graph API calls to a third-party proxy service by changing the request host and substituting a Yuri platform token for the Facebook access token. It is intended for users who have verified the provider and are comfortable making baiz.ai part of their Facebook security boundary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill routes Facebook Graph API traffic through a third-party gateway that can affect Facebook requests and token handling. <br>
Mitigation: Install only after deciding to trust baiz.ai as part of the Facebook security boundary, start with a least-privilege test Facebook account, and verify provider security and revocation controls before production use. <br>
Risk: Write, delete, upload, publishing, ads, or account-management operations could change Facebook assets through the proxy. <br>
Mitigation: Require human approval before any state-changing or account-management request and review the exact endpoint, method, parameters, and target account. <br>
Risk: Passing a sensitive token as an access_token query parameter can expose it through browser history or logs. <br>
Mitigation: Prefer sending the token in POST or PUT request bodies when supported, store it only in a secret manager or environment variable, and rotate or revoke it if exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuriskills/yuri-graph-gateway) <br>
- [Publisher profile](https://clawhub.ai/user/yuriskills) <br>
- [baiz.ai homepage](https://baiz.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown usage guidance with curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Describes credential handling, proxy endpoint substitution, supported request types, and security precautions.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
