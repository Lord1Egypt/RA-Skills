## Description: <br>
Make HTTP requests (GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS) with custom headers, automatic retries, and graceful error handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stephen-standridge](https://clawhub.ai/user/stephen-standridge) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to call APIs, fetch URLs, send webhooks, and make HTTP requests without external dependencies. It is useful when requests need custom headers, retries, timeout handling, and inspectable responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send authenticated or state-changing HTTP requests. <br>
Mitigation: Require explicit confirmation before POST, PUT, PATCH, or DELETE requests against real systems. <br>
Risk: Requests may expose secrets or personal data to untrusted destinations. <br>
Mitigation: Verify destination URLs before use and send secrets only to trusted endpoints with scoped temporary tokens. <br>
Risk: Automatic retries can repeat transiently failing requests. <br>
Mitigation: Use conservative retry settings for non-idempotent operations and inspect failed responses before retrying manually. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/stephen-standridge/simplehttpskill) <br>
- [Publisher profile](https://clawhub.ai/user/stephen-standridge) <br>


## Skill Output: <br>
**Output Type(s):** [code, API calls, configuration, guidance] <br>
**Output Format:** [JavaScript module usage with structured response objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses include ok, status, headers, body, and error fields; JSON response bodies are parsed when content type indicates JSON.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
