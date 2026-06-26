## Description: <br>
Automates ZenTao work-hour reporting by matching a user's work description to tasks, confirming the match, and recording time through the ZenTao API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[crecendow](https://clawhub.ai/user/crecendow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Team members who track work in ZenTao use this skill to turn natural-language daily work descriptions into confirmed task matches and recorded work-hour entries. It can fetch task lists, calculate remaining hours, and submit recordworkhour updates after user confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires ZenTao account access and can modify work-hour records. <br>
Mitigation: Install only for environments where this access is acceptable, confirm task matches before submission, and prefer a scoped token or dedicated account where possible. <br>
Risk: The security review reports exposed live login session handling and credential practices that need review. <br>
Mitigation: Before production use, remove zentaosid logging, require HTTPS for ZENTAO_URL, avoid /tmp/cookies.txt, and restrict permissions on the .env file. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/crecendow/zentao-autoreport) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style task match summaries, command guidance, and script status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke local Python or shell scripts that read ZenTao configuration, authenticate, fetch tasks, and submit work-hour updates.] <br>

## Skill Version(s): <br>
1.0.2 (source: server evidence release version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
