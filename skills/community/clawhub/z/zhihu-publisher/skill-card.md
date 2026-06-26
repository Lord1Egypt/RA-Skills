## Description: <br>
Automates Zhihu article publishing by guiding an agent through Chrome-based login, article editing, formatting, and posting with xbrowser. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuxucai](https://clawhub.ai/user/liuxucai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to have an agent operate a logged-in Chrome session to draft, format, and publish long-form articles on Zhihu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish publicly to a user's Zhihu account from a logged-in Chrome session. <br>
Mitigation: Require the agent to show the final article title and content and receive explicit user approval before clicking publish. <br>
Risk: Account credentials and logged-in browser access are involved during setup and use. <br>
Mitigation: Provide credentials interactively, do not store them in files, and use only a browser session/account intended for the publishing task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liuxucai/zhihu-publisher) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown with bash and JavaScript command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires xbrowser with Chrome and an active user-controlled Zhihu account session; long article text is inserted in chunks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
