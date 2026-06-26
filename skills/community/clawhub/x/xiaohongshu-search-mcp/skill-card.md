## Description: <br>
Search XiaoHongShu / RED notes through the hosted whatson.red MCP endpoint when users need structured RED search results, note details, or a draft blog payload. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seichris](https://clawhub.ai/user/seichris) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search XiaoHongShu / RED / RedNote through whatson.red and retrieve structured notes, note details, usage data, and optional draft blog content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: whatson.red receives search queries and the Agent API key used for MCP requests. <br>
Mitigation: Install only if the user trusts whatson.red, and prefer a scoped or revocable API key where available. <br>
Risk: High result limits can increase account credit usage. <br>
Mitigation: Monitor remaining credits and choose result limits that match the user's task. <br>
Risk: The optional blog payload may be mistaken for published content. <br>
Mitigation: Treat blog output as a draft and review it before any separate publishing workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/seichris/xiaohongshu-search-mcp) <br>
- [whatson.red Agents](https://www.whatson.red/agents) <br>
- [whatson.red MCP endpoint](https://www.whatson.red/api/agent/mcp) <br>
- [whatson.red REST search endpoint](https://www.whatson.red/api/agent/search) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration instructions, API Calls, JSON, Markdown] <br>
**Output Format:** [Markdown guidance with JSON-oriented MCP and REST request and response details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WHATSON_RED_API_KEY; optional blog output is a draft payload and is not published by the skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
