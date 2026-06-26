## Description: <br>
Comprehensive cybersecurity technology stack recommendation platform that generates personalized security tool recommendations based on organizational assessment data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security architects, CISO offices, compliance officers, cloud architects, and IT teams use this skill to generate cybersecurity stack recommendations from organizational size, industry, budget, maturity, deployment, cloud, compliance, and priority inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends organizational security assessment content and identifiers to an external service. <br>
Mitigation: Avoid confidential security posture, compliance scope, vendor-selection details, and real user identifiers unless appropriate privacy, security, retention, and access-control terms are in place. <br>
Risk: Generated recommendations may influence security architecture, compliance planning, and vendor selection. <br>
Mitigation: Have qualified security and compliance reviewers validate recommendations, cost estimates, and implementation phases before operational use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/krishnakumarmahadevan-cmd/toolweb-security-stack-builder) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [OpenAPI specification](artifact/openapi.json) <br>
- [API documentation](https://api.mkkpro.com:8122/docs) <br>
- [Security Stack Builder API route](https://api.mkkpro.com/security/security-stack-builder) <br>
- [ToolWeb](https://toolweb.in) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [JSON API responses documented in Markdown, including recommendation categories, tool rationales, compliance mappings, cost estimates, and implementation phases.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires organizational assessment data and may include session, timestamp, and optional user identifiers in requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and OpenAPI info.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
