## Description: <br>
Send X5 protocol API requests from the terminal, parse .x5 files, generate X5 cURL commands, and debug X5 service endpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[growingppp](https://clawhub.ai/user/growingppp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create, inspect, and send X5 protocol API requests from .x5 files or inline parameters during endpoint testing and debugging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: .x5 files and inline parameters can direct the client to arbitrary URLs with custom headers and bodies. <br>
Mitigation: Review the target URL, headers, body, method, appid, and appkey before sending a request. <br>
Risk: Credentials or encoded request details may appear in terminal history, logs, dry-run output, or generated cURL commands. <br>
Mitigation: Use short-lived credentials where possible and avoid sharing terminals, logs, dry-run output, or generated cURL commands that contain secrets. <br>
Risk: Requests to non-local endpoints over plaintext HTTP can expose request data and credentials. <br>
Mitigation: Prefer HTTPS for non-local services and reserve localhost HTTP examples for local testing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/growingppp/x5-protocol) <br>
- [Publisher profile](https://clawhub.ai/user/growingppp) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON results, and generated cURL commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read .x5 request files or inline parameters and may emit encoded request details during dry runs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
