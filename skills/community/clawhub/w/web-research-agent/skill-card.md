## Description: <br>
Use OpenMarlin from OpenClaw to answer questions, run tasks, and manage OpenMarlin account setup and billing flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[emcraig51](https://clawhub.ai/user/emcraig51) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and OpenClaw operators use this skill to register or connect an OpenMarlin account, submit routed executions, run asynchronous video tasks, and manage prepaid billing recovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles persistent OpenMarlin platform API keys. <br>
Mitigation: Use OpenClaw auth-profile storage where available, avoid exposing raw secrets in chat or logs, and rotate any API key that may have been printed or captured. <br>
Risk: The skill can trigger remote executions, video tasks, top-ups, referral lookups, and checkout flows. <br>
Mitigation: Require explicit user approval before those actions and keep external browser use limited to identity or Stripe checkout steps. <br>
Risk: A misconfigured OpenMarlin server URL could send registration, execution, billing, or credential flows to the wrong endpoint. <br>
Mitigation: Verify that OPENMARLIN_SERVER_URL is the intended bare API origin before registration or authenticated requests. <br>
Risk: Server-resolved GitHub import provenance is unavailable for this release. <br>
Mitigation: Install only if the user intends to use OpenMarlin and trusts the server-resolved publisher and release source. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/emcraig51/web-research-agent) <br>
- [Publisher Profile](https://clawhub.ai/user/emcraig51) <br>
- [OpenMarlin API Origin](https://api.openmarlin.ai) <br>
- [OpenMarlin Website](https://openmarlin.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May initiate OpenMarlin API calls, registration polling, task polling, and billing recovery flows when explicitly requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
