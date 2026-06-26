## Description: <br>
Search and analyze your own session logs (older/parent conversations) using jq. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guogang1024](https://clawhub.ai/user/guogang1024) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to search prior local conversation logs, extract messages, summarize cost, and inspect tool usage when historical context is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can surface sensitive or unrelated content from older local session logs. <br>
Mitigation: Limit searches by date, topic, or session, and avoid exposing unrelated sensitive content from prior conversations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guogang1024/session-logs) <br>
- [Publisher profile](https://clawhub.ai/user/guogang1024) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local jq and rg binaries and access to the agent's local session JSONL files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
