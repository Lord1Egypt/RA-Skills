## Description: <br>
Helps agents configure WeFlow API access, monitor selected WeChat groups, and summarize new group messages on a recurring heartbeat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liusining](https://clawhub.ai/user/liusining) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers who control a WeFlow account can use this skill to set up WeChat group monitoring, maintain group configuration, and produce periodic summaries of new messages and selected members' posts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional unauthenticated LAN proxy can expose WeFlow chat and media endpoints to other machines on the network. <br>
Mitigation: Use the proxy only when remote access is required, run it on a trusted network, and restrict firewall access to the intended client machine. <br>
Risk: The skill processes private WeChat group messages and may download image media to local paths. <br>
Mitigation: Install only when the operator controls the WeFlow account and has permission to summarize the selected groups; keep configuration files and downloaded media in a private directory. <br>
Risk: Unpinned Python dependencies may resolve to different package versions over time. <br>
Mitigation: Pin PyYAML and openpyxl to current patched versions before deployment. <br>


## Reference(s): <br>
- [WeFlow HTTP API](reference/HTTP-API.md) <br>
- [WeFlow Desktop](https://github.com/hicccc77/WeFlow) <br>
- [ChatLab Format](https://github.com/nichuanfang/chatlab-format) <br>
- [ClawHub Skill Page](https://clawhub.ai/liusining/weflow-group-summarizer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and generated configuration or message-summary text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local image file paths for the agent to inspect when WeFlow exports media from group messages.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
