## Description: <br>
Generate cost and token usage reports from OpenClaw session logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[directorvector](https://clawhub.ai/user/directorvector) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to summarize API cost, token usage, billing, spending, and daily or session-level usage from local OpenClaw session JSONL logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local OpenClaw session logs, which may reveal private session names or usage patterns. <br>
Mitigation: Run it only on session logs you intend to inspect, keep generated reports local when usage details are sensitive, and use OPENCLAW_SESSIONS_DIR to point at an appropriate log directory. <br>
Risk: The report depends on local jq and bc binaries. <br>
Mitigation: Install jq and bc before running the script and review any command output before sharing it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/directorvector/usage-report) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Text or JSON usage report with shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports can cover all sessions, today, or a specific UTC date; totals include turns, cost, token counts, and cache read/write tokens.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
