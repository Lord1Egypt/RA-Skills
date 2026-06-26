## Description: <br>
Build agents that learn from user corrections by updating and following dated rules to improve performance and reduce repeated mistakes over time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amdf01-debug](https://clawhub.ai/user/amdf01-debug) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add a correction loop where an agent records reusable user corrections in RULES.md, reviews them later, and reduces repeated mistakes over time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local rules can capture stale, overly specific, or sensitive correction details. <br>
Mitigation: Review each new RULES.md entry, keep rules general, avoid secrets and client-specific personal details, and prune outdated entries periodically. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/amdf01-debug/sw-self-improving-agent) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration] <br>
**Output Format:** [Markdown guidance with example RULES.md and AGENTS.md snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local operating-rule guidance; users review saved rules before relying on them.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
