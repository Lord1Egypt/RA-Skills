## Description: <br>
Search and analyze your own session logs (older/parent conversations) using jq. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to search local JSONL session transcripts, recover context from earlier conversations, inspect message history, and summarize session costs or tool usage. It is intended for scoped local analysis of the user's own conversation logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Session transcript searches can expose sensitive conversation history beyond what the user intended to review. <br>
Mitigation: Keep searches scoped to the requested session, date, or phrase, and confirm scope before broad all-session searches. <br>
Risk: Session logs may contain credentials, API keys, tokens, or other secrets pasted during prior debugging. <br>
Mitigation: Do not display secret values; note their presence and recommend rotation when real credentials are found. <br>
Risk: Sending session log contents to network commands or remote destinations can disclose private transcripts. <br>
Mitigation: Process logs locally and avoid piping or redirecting transcript contents to network-transmitting tools. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/snazar-faberlens/session-logs-hardened) <br>
- [Faberlens safety evaluation](https://faberlens.ai/explore/session-logs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with jq and ripgrep shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local jq and rg; output should keep session-log searches scoped and local.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
