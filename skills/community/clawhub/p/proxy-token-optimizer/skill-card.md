## Description: <br>
Optimize LLM token usage and API costs for the openclaw-manager proxy platform with model-tier routing, heartbeat cost reduction, context lazy loading, and platform usage analytics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whyhit2005](https://clawhub.ai/user/whyhit2005) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to route prompts to cost-appropriate models, reduce heartbeat spend, generate lazy-loading agent context guidance, and analyze PostgreSQL-backed usage records for quota planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Usage and quota reports may expose sensitive operational data. <br>
Mitigation: Run DB-backed reporting commands only with authorization and handle generated reports as sensitive operational data. <br>
Risk: Generated AGENTS.md.optimized guidance could change live agent context-loading behavior. <br>
Mitigation: Review AGENTS.md.optimized before adopting it as live agent instructions. <br>
Risk: The skill is intended for the openclaw-manager environment. <br>
Mitigation: Install and run it only in the intended openclaw-manager deployment context. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/whyhit2005/proxy-token-optimizer) <br>
- [Publisher profile](https://clawhub.ai/user/whyhit2005) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, code, shell commands, configuration] <br>
**Output Format:** [JSON reports, Markdown agent guidance, shell command recommendations, and configuration patches] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local routing, context, and heartbeat commands can run without network access; usage reports and quota advice require authorized database access.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
