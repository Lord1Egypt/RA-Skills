## Description: <br>
RedLine provides usage-pacing guidance for agents that check Claude.ai and OpenAI subscription budgets and throttle work as limits approach. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wgj](https://clawhub.ai/user/wgj) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use RedLine to monitor Claude.ai and OpenAI subscription usage and adjust autonomous work intensity before rate limits are exhausted. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents to repeatedly use local Claude/OpenAI OAuth credentials through usage-checking scripts that were not included for review. <br>
Mitigation: Do not wire it into heartbeat automation until the actual scripts are present, reviewed, pinned to the expected path, and confirmed not to print, store, or send tokens anywhere except the intended provider endpoints. <br>
Risk: Credential-backed provider usage checks can expose sensitive local tokens if the installed scripts differ from the documented behavior. <br>
Mitigation: Install only after reviewing the scripts and only in environments where access to the local Claude Code Keychain token and OpenClaw OpenAI auth profile is acceptable. <br>


## Reference(s): <br>
- [RedLine on ClawHub](https://clawhub.ai/wgj/redline) <br>
- [README](README.md) <br>
- [Skill Instructions](SKILL.md) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3; documented usage checks rely on local Claude/OpenAI OAuth credentials and provider usage APIs.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
