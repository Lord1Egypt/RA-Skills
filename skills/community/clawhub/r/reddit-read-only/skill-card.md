## Description: <br>
Browse and search Reddit in read-only mode using public JSON endpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tristanmanchester](https://clawhub.ai/user/tristanmanchester) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, agents, and external users use this skill to find Reddit posts, search topics, inspect comment threads, and collect permalinks for manual review or replies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local Node script sends requested subreddit names, search terms, and post URLs to Reddit public endpoints. <br>
Mitigation: Use the skill only for queries you are comfortable sending to reddit.com, and avoid entering sensitive or private search terms. <br>
Risk: Reddit may return incomplete, rate-limited, or HTML responses instead of JSON. <br>
Mitigation: Start with small limits, reduce request volume when failures occur, and use the documented pacing environment variables when repeated requests are needed. <br>
Risk: The skill is read-only and cannot post replies, vote, moderate, or authenticate as a Reddit user. <br>
Mitigation: Use the generated permalinks to inspect Reddit manually and perform any account actions outside the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tristanmanchester/reddit-read-only) <br>
- [Output schema](references/OUTPUT_SCHEMA.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [JSON from shell commands, with Markdown summaries and permalinks presented by the agent] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Command output is read-only Reddit data shaped as ok/data or ok/error JSON; comment and post text is returned as snippets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
