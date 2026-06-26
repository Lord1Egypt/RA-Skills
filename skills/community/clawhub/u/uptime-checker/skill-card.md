## Description: <br>
Lightweight URL uptime checker and response time monitor for checking websites and APIs, measuring response times, tracking history, and detecting SSL issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Johnnywang2001](https://clawhub.ai/user/Johnnywang2001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to check whether websites or API endpoints are reachable, confirm expected HTTP status codes, measure response time, and generate simple uptime history summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Custom headers and saved history can expose private service URLs or credentials if used carelessly. <br>
Mitigation: Use Authorization or Cookie headers only with trusted endpoints and keep saved history files private. <br>
Risk: Disabling SSL verification can hide certificate problems. <br>
Mitigation: Keep SSL verification enabled by default and use --no-verify-ssl only for known internal or self-signed endpoints. <br>
Risk: Non-read-only HTTP methods can have side effects on some endpoints. <br>
Mitigation: Prefer GET or HEAD for routine uptime checks unless the endpoint is explicitly designed for another method. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Johnnywang2001/uptime-checker) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; runtime output is text tables or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can save local history files and exits with status 1 when any checked endpoint is down.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
