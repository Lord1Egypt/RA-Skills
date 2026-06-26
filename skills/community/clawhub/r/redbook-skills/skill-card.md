## Description: <br>
Automates Xiaohongshu (XHS/RED) content publishing and supports login checks, content discovery, engagement actions, and content data retrieval. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[cp3d1455926-svg](https://clawhub.ai/user/cp3d1455926-svg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, marketers, and developers use this skill to prepare, preview, publish, and inspect Xiaohongshu content from an agent workflow. It can also run account checks, collect feed or profile data, and perform engagement actions after the user confirms the target content or action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can act on a live Xiaohongshu account and publish by default. <br>
Mitigation: Use preview or fill-only workflows first, then verify the selected account, title, body, media, and engagement target before any publish or interaction command. <br>
Risk: Login QR output, Chrome profiles, notification payloads, and exported analytics may expose sensitive account data. <br>
Mitigation: Treat those outputs and local profiles as sensitive, avoid sharing them, and remove exported data when it is no longer needed. <br>
Risk: Remote CDP can give the skill control over a browser endpoint outside the local machine. <br>
Mitigation: Use remote CDP only with trusted endpoints and confirm the endpoint host, port, and active account before running commands. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/cp3d1455926-svg/redbook-skills) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>
- [Claude Code integration guide](artifact/docs/claude-code-integration.md) <br>
- [Quick start guide](artifact/快速上手指南.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and text guidance with shell command examples, structured command results, and optional CSV or Markdown files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May operate a browser session logged in to Xiaohongshu; preview and fill-only workflows are available before publishing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
