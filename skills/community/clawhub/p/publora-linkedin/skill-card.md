## Description: <br>
Post or schedule LinkedIn content through the Publora API, retrieve analytics, manage reactions, post comments, and mention people or organizations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sergebulaev](https://clawhub.ai/user/sergebulaev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and social media operators use this skill to have an agent provide Publora API guidance and request examples for publishing or scheduling LinkedIn posts, checking analytics, managing reactions, and creating or deleting comments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide actions that publish, comment, react, schedule, or delete content on a real LinkedIn account. <br>
Mitigation: Require explicit confirmation of the account, content, target post, target comment or reaction, deletion target, and scheduled time before any mutating request. <br>
Risk: A Publora API key can authorize account actions if exposed or misused. <br>
Mitigation: Store the Publora API key securely and use the least-privileged connected account practical. <br>
Risk: Publora LinkedIn API limits and platform quirks can cause failed requests or unexpected output formatting. <br>
Mitigation: Check documented media limits, supported formats, rate limits, query type requirements, and LinkedIn formatting constraints before sending requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sergebulaev/publora-linkedin) <br>
- [Publora API base URL](https://api.publora.com/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown with JavaScript fetch examples, API parameters, and confirmation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Publora API endpoints, request bodies, platform IDs, scheduling timestamps, analytics query types, post or comment IDs, and confirmation prompts for mutating actions.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
