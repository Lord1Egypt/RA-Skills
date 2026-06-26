## Description: <br>
xyq helps agents support image and video creation workflows for Pippit and Xiaoyunque, including request submission, generation-status checks, and returning generated asset links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imaoda](https://clawhub.ai/user/imaoda) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and creators use this skill through an agent to generate or edit images and videos, select the correct regional service, submit generation requests, and retrieve completed media assets. Developers may also use it to prepare request payloads and configuration needed for those workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill appears to require users to provide live browser session cookies and store them locally, creating account-takeover risk if those cookies are exposed or mishandled. <br>
Mitigation: Install only when session-level account access is acceptable; prefer OAuth or API-token flows, use disposable or low-privilege accounts where possible, rotate or delete stored cookies after use, and never paste cookies into shared chats or logs. <br>
Risk: Generation results may require asynchronous polling and can be slow, especially for video workflows. <br>
Mitigation: Set clear polling limits, report intermediate status to the user, and stop polling when a terminal state or timeout is reached. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/imaoda/xyq) <br>
- [Pippit home](https://www.pippit.ai/home) <br>
- [Xiaoyunque home](https://xyq.jianying.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown responses with generated JSON request bodies, shell command usage, configuration guidance, and generated asset links when available] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May rely on asynchronous polling for image or video generation results.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
