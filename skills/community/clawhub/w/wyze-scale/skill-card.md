## Description: <br>
Read body metrics from a Wyze smart scale, including weight, BMI, body fat, water, muscle, and BMR, with support for multiple household members. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[noelportugal](https://clawhub.ai/user/noelportugal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users and agents use this skill to retrieve recent Wyze scale readings, weigh-in history, and household member scale records for private body-metrics questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose sensitive body metrics and health-related account data. <br>
Mitigation: Use it only in private conversations, share readings only with the relevant account owner, and avoid group or shared surfaces. <br>
Risk: The skill requires an API token for a health-related account. <br>
Mitigation: Protect the token, install only when this access is intended, and revoke or rotate the token when access is no longer needed. <br>
Risk: The Wyze API integration is unofficial and may break if Wyze changes its API. <br>
Mitigation: Review results before relying on them and refresh or update the integration when authentication or API calls fail. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/noelportugal/wyze-scale) <br>
- [wyze-node package](https://www.npmjs.com/package/wyze-node) <br>
- [Wyze developer API console](https://developer-api-console.wyze.com/#/apikey/view) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text responses from a Node CLI, with setup guidance in Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node, wyze-node, Wyze API credentials, and a cached login token.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
