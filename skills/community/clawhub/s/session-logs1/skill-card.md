## Description: <br>
Search and analyze your own session logs (older/parent conversations) using jq. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yanjiang8124](https://clawhub.ai/user/yanjiang8124) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to find prior conversations, inspect session transcripts, summarize costs, and search historical tool or message activity in local session logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Searching local session transcripts can expose sensitive past chat content or old tool outputs. <br>
Mitigation: Use specific dates, session IDs, or keywords and avoid importing unrelated transcript content into the current conversation. <br>
Risk: Commands read local OpenClaw session files under the user's home directory. <br>
Mitigation: Review proposed shell commands before execution and run them only against the intended session paths. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yanjiang8124/session-logs1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash and jq command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local access to OpenClaw session JSONL files and the jq and rg command-line tools.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
