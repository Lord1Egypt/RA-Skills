## Description: <br>
搜索助手免费版 helps individual users split complex research questions into up to five search subtasks, dispatch them to a general search agent, and aggregate the results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to decompose broad research, market, product, or technical comparison questions into focused search subtasks and combine the findings into a structured answer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries and generated subqueries may be sent to external search or fetch services. <br>
Mitigation: Avoid confidential prompts and review generated subqueries before allowing external search or fetch calls. <br>
Risk: The skill requests broad read, exec, glob, and grep authority. <br>
Mitigation: Install only with the minimum tool authority needed for the intended search workflow. <br>
Risk: SEO, ranking, callback, and capability language is unclear or outside the core research-helper use case. <br>
Mitigation: Use the skill for research decomposition and aggregation, and reject workflows that attempt search-engine manipulation or unreviewed callbacks. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/thcjp/skills/search-assistant-tool-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown report with task decomposition and aggregated search results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Limits decomposition to five subtasks and relies on a general search capability.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
