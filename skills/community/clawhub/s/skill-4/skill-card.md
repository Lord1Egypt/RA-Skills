## Description: <br>
Lightweight website uptime monitor. Check if URLs are up, measure response times, detect content changes via hashing, and verify expected content. Zero dependencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[claudiodrusus](https://clawhub.ai/user/claudiodrusus) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and site operators use this skill to check website availability, response time, expected status codes, expected page content, and content hash changes for one or more URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests to URLs provided by the user. <br>
Mitigation: Provide only URLs you are authorized to test, and avoid internal, private admin, localhost, or cloud metadata URLs unless that access is intentional. <br>
Risk: Monitoring results can be misleading when the expected status code, timeout, content string, or prior hash is stale or incorrect. <br>
Mitigation: Confirm monitoring parameters before relying on results for alerts, automation, or operational decisions. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text or JSON results, with shell command examples when invoked by an agent.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports URL, HTTP status, response time, content length, content hash, change status, text-match status, and errors; exits with code 1 when any checked site fails expectations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
