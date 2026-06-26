## Description: <br>
REST API Tester helps agents test REST endpoints, validate responses, benchmark performance, run OpenAPI-based checks, and generate HTML reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ericlooi504](https://clawhub.ai/user/ericlooi504) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to exercise REST endpoints, validate status, timing, and response keys, benchmark latency, test OpenAPI specs, and create shareable reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requests can send Authorization headers, request bodies, or state-changing methods to the wrong endpoint. <br>
Mitigation: Use staging endpoints and least-privilege test tokens when possible, verify URLs before sending sensitive data, and review POST, PUT, PATCH, DELETE, benchmark, and test-all runs before execution. <br>
Risk: Verbose output or generated HTML reports can contain secrets, personal data, or internal API details. <br>
Mitigation: Review generated reports before sharing them and delete report files when they may contain sensitive response data. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Files] <br>
**Output Format:** [Markdown with inline bash commands and optional HTML report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate local HTML reports that include API response data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
