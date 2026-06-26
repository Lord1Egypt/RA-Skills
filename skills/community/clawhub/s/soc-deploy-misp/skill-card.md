## Description: <br>
Deploy MISP threat intelligence platform on any Docker-ready Linux host using the official misp-docker project with automatic MariaDB memory tuning, API key generation via cake CLI, and credential management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[solomonneas](https://clawhub.ai/user/solomonneas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, SOC engineers, and security operators use this skill to deploy a MISP threat intelligence platform on an existing Docker-ready Linux host and receive connection details for follow-on automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The deployment flow uses unsafe credential defaults and writes secrets to local files. <br>
Mitigation: Use a strong unique admin password, restrict or delete ~/misp/api-key.txt after setup, lock down .env permissions, and rotate exposed secrets. <br>
Risk: The generated connection guidance relies on self-signed TLS and disabled certificate verification. <br>
Mitigation: Configure trusted TLS certificates or a trusted reverse proxy before production use instead of relying on curl -k or MISP_VERIFY_SSL=false. <br>
Risk: Pulling the latest misp-docker state can change deployment behavior over time. <br>
Mitigation: Pin the misp-docker version for production deployments and review changes before upgrading. <br>


## Reference(s): <br>
- [MISP Docker project](https://github.com/MISP/misp-docker.git) <br>
- [MISP deployment gotchas](references/gotchas.md) <br>
- [MISP environment template](references/env-template.env) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown with inline bash commands and deployment details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes generated credentials, API key details, service URL, and TLS verification notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
