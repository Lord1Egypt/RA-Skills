## Description: <br>
Monitors conversation state, sends follow-up responses when a chat may stall, reports progress for long tasks, and supports configurable multi-platform chat integrations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wwwsyber](https://clawhub.ai/user/wwwsyber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to add local conversation monitoring, automatic follow-up, progress reporting, and configurable platform adapters to chat-oriented agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer can create persistent local service behavior. <br>
Mitigation: Review installation steps before enabling service mode, and run the skill directly unless persistence is required. <br>
Risk: Conversation profiling, prediction, learning, and logging can expose sensitive user behavior or chat content. <br>
Mitigation: Disable training, learning, platform broadcasting, and unnecessary logging unless explicitly needed for the deployment. <br>
Risk: Automatic responses may send unintended messages across configured chat platforms. <br>
Mitigation: Start with conservative thresholds and test platform integrations in a non-production workspace before enabling live responses. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wwwsyber/syberz-chatflow-guardian) <br>
- [Publisher profile](https://clawhub.ai/user/wwwsyber) <br>
- [README](README.md) <br>
- [English README](README_EN.md) <br>
- [Security policy](SECURITY.md) <br>
- [Changelog](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JavaScript, JSON, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local monitoring behavior, progress messages, generated responses, logs, and configuration guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, changelog, server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
