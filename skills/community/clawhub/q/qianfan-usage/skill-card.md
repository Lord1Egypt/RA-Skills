## Description: <br>
Queries Baidu Qianfan Coding Plan usage and quotas, with optional browser-assisted login and saved session reuse. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wsjwoods](https://clawhub.ai/user/wsjwoods) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers using Baidu Qianfan Coding Plan use this skill to check short-term, weekly, and monthly quota consumption from the command line and to refresh login state when cookies expire. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reusable Baidu session cookies are stored on the local machine. <br>
Mitigation: Treat ~/.baidu-qianfan-auth.json like a password, avoid shared systems, and delete it when finished. <br>
Risk: Runtime command wiring may reference the removed qianfan-usage.sh script. <br>
Mitigation: Review command mapping before relying on the /qianfan-usage command in an agent environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wsjwoods/qianfan-usage) <br>
- [Baidu Qianfan quota API endpoint](https://console.bce.baidu.com/api/qianfan/charge/codingPlan/quota) <br>
- [agent-browser dependency](https://github.com/nicepkg/agent-browser) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text with quota values, reset times, status messages, and command-line setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May store and reuse Baidu session cookies in ~/.baidu-qianfan-auth.json.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
