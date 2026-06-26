## Description: <br>
Retrieves the device's current public IP address by running a Python script. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ZhangEnsure](https://clawhub.ai/user/ZhangEnsure) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users and operators use this skill to check the current public IP address visible from the local machine. It is useful for network troubleshooting, connectivity checks, and confirming outbound IP identity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public IP lookup services receive the request and can observe the caller's public IP address. <br>
Mitigation: Use only where outbound requests to public IP lookup services are acceptable, or replace the endpoints with an approved internal service. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands] <br>
**Output Format:** [Plain text public IP address or failure message] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs a Python 3 script that makes outbound HTTPS requests to public IP lookup services.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
