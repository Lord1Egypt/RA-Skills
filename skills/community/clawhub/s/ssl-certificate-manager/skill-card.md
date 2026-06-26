## Description: <br>
Automate SSL certificate generation and management with DNS challenge validation and certificate provisioning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security professionals, DevOps teams, and infrastructure engineers use this skill to generate DNS challenges, request SSL/TLS certificates, download certificate files, and debug domain validation for domains they control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can issue certificates and retrieve private keys without clearly documented authentication, authorization, or key-handling safeguards. <br>
Mitigation: Use it only for domains you control, verify strong provider authentication and per-domain authorization, start with staging certificates, and keep private keys in a secret manager rather than logs or agent output. <br>
Risk: Certificate generation against the wrong domain or environment can create operational or trust-management impact. <br>
Mitigation: Review DNS challenge records before certificate requests and use the debug endpoint and staging option before production issuance. <br>


## Reference(s): <br>
- [OpenAPI specification](artifact/openapi.json) <br>
- [API docs](https://api.mkkpro.com:8044/docs) <br>
- [Kong route](https://api.mkkpro.com/security/ssl-certificate-manager) <br>
- [ClawHub skill page](https://clawhub.ai/krishnakumarmahadevan-cmd/ssl-certificate-manager) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with JSON request and response examples, plus downloadable certificate files from the API] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses domain and email inputs for DNS challenge creation and certificate generation; certificate downloads may include PEM, private key, or chain files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
