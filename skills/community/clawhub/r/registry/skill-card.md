## Description: <br>
Search Sharebench, an open registry of reusable AI artifacts including skills, agent personas, prompts, and playbooks in SKILL.md format. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sharebench](https://clawhub.ai/user/sharebench) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and agent operators use this skill to search the public Sharebench registry for reusable open-licensed artifacts before building a capability from scratch. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Sharebench over the network. <br>
Mitigation: Avoid secrets, confidential customer data, and private project details in search queries. <br>
Risk: Returned artifacts may not fit the user's exact context or may need attribution preserved. <br>
Mitigation: Read each returned artifact fully, adapt it to the current task, and preserve author attribution and visible provenance when reusing it. <br>


## Reference(s): <br>
- [ClawHub listing for Sharebench registry](https://clawhub.ai/sharebench/skills/registry) <br>
- [Sharebench public search API](https://sharebench.ai/api/public/search?q=YOUR+QUERY) <br>
- [Sharebench MCP endpoint](https://mcp-public.sharebench.ai) <br>
- [Sharebench](https://sharebench.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Markdown, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON response descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results are returned by Sharebench as anonymous, rate-limited JSON; full artifacts should be read before reuse.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
