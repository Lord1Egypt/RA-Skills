## Description: <br>
Post or schedule content to Facebook Pages using the Publora API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sergebulaev](https://clawhub.ai/user/sergebulaev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and social media operators use this skill to have an agent prepare guidance and API examples for publishing or scheduling Facebook Page posts through Publora. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Publora API keys could be exposed or misused if pasted into shared conversations, logs, or generated files. <br>
Mitigation: Keep API keys private, avoid storing secrets in generated artifacts, and rotate or revoke access when the integration is no longer needed. <br>
Risk: Incorrect Page IDs, media choices, or scheduled times could publish content to the wrong destination or at the wrong time. <br>
Mitigation: Verify the Facebook Page platform ID, post content, media constraints, and scheduled timestamp before any API call is made. <br>
Risk: Publora or Facebook token state can cause posting failures after permission changes or token refresh problems. <br>
Mitigation: Reconnect the Facebook Page in the dashboard and confirm permissions before retrying failed publishing workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sergebulaev/publora-facebook) <br>
- [Publora API base URL](https://api.publora.com/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, API calls, configuration] <br>
**Output Format:** [Markdown with JavaScript fetch examples and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a private Publora API key and Facebook Page platform ID supplied by the user.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
