## Description: <br>
Generate, manage, and download SSL/TLS certificates with token-based verification and multi-domain support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, DevOps teams, security engineers, and automation platforms use this skill to work with a certificate-management API for token generation, domain verification, certificate issuance, and certificate file downloads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Certificate and private-key downloads are highly sensitive. <br>
Mitigation: Verify provider trust and confirm how private keys are generated, stored, retained, audited, protected, and downloaded before using the API for real domains. <br>
Risk: Certificate issuance for real domains depends on strong authentication, authorization, and domain ownership proof. <br>
Mitigation: Confirm that the API enforces authentication, verifies domain ownership, and authorizes certificate and private-key downloads before production use. <br>


## Reference(s): <br>
- [Certificaty API route](https://api.toolweb.in/tools/certificaty) <br>
- [Certificaty API documentation](https://api.toolweb.in:8164/docs) <br>
- [ToolWeb](https://toolweb.in) <br>
- [ToolWeb OpenClaw](https://toolweb.in/openclaw/) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Files, Guidance] <br>
**Output Format:** [Markdown guidance with JSON request and response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference certificate and private-key file downloads that require careful handling.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
