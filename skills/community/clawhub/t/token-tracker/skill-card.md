## Description: <br>
Track and report token usage and cost for conversations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zty-f](https://clawhub.ai/user/zty-f) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent for current conversation token usage, estimated cost, cache hit rate, and context utilization summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may respond to broad cost or usage wording, or after longer tasks, when the user only wants on-demand reports. <br>
Mitigation: Use narrower trigger wording or invoke it explicitly when a token or cost summary is desired. <br>
Risk: Cost information is an estimate unless the current session status provides authoritative cost data. <br>
Mitigation: Treat session status as authoritative and present static pricing tables only as reference material. <br>


## Reference(s): <br>
- [Publisher profile: zty-f](https://clawhub.ai/user/zty-f) <br>
- [Skill listing: Token Tracker](https://clawhub.ai/zty-f/token-tracker) <br>
- [Author blog](https://www.zruler.fun/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown summary of current conversation usage metrics and cost estimates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports current session metrics only; actual cost from session status is authoritative when available.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
