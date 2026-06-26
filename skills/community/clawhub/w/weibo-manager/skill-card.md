## Description: <br>
Manage Weibo posts through Puppeteer with a request, approval, and execution workflow for publishing text and images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HMyaoyuan](https://clawhub.ai/user/HMyaoyuan) <br>

### License/Terms of Use: <br>
ISC <br>


## Use Case: <br>
Developers and operators use this skill to draft Weibo posts, send them for human approval, and publish approved text and image posts through an authenticated browser session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses reusable Weibo session cookies stored in cookies.json. <br>
Mitigation: Protect the cookie file as a secret, limit filesystem access to it, and rotate or remove the session when the skill is no longer needed. <br>
Risk: The release includes under-disclosed delete and diagnostic scripts in addition to the documented approval workflow. <br>
Mitigation: Remove or disable delete and diagnostic scripts before use unless they are explicitly reviewed and needed. <br>
Risk: Some helper calls are built through shell command strings. <br>
Mitigation: Review inputs before execution and replace shell-built subprocess calls with argument-array APIs before deployment. <br>
Risk: Publishing, deleting, screenshot upload, and local image processing can affect external accounts or expose local content. <br>
Mitigation: Require explicit human confirmation before those actions and review any image paths or screenshots before they are uploaded. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/HMyaoyuan/weibo-manager) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, API Calls, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON task files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates pending post JSON files and sends approval or status messages through Feishu integrations.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
