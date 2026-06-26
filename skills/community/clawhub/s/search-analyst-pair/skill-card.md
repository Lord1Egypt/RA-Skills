## Description: <br>
Turn any research request into a structured, reviewable brief: fact collection, risk analysis, and recommendation in three deterministic steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baobaodawang-creater](https://clawhub.ai/user/baobaodawang-creater) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams running self-hosted OpenClaw use this skill to route `/hunt` research requests through fixed search, analysis, and synthesis stages for traceable decision support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research prompts and findings may be exposed to the configured OpenClaw agents and their underlying providers. <br>
Mitigation: Install only with trusted main, search, and analyst agents and use a scoped OpenClaw token. <br>
Risk: External runtime workflow assets may differ from the registry-facing documentation. <br>
Mitigation: Verify the runtime workflow assets before relying on the skill for operational decisions. <br>
Risk: Overbroad agent-to-agent permissions could route research content beyond the intended workflow. <br>
Mitigation: Keep subagent allowlists narrow and limited to the documented main, search, and analyst handoffs. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/baobaodawang-creater/search-analyst-pair) <br>
- [Homepage](https://github.com/baobaodawang-creater/neo-agent-lab) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown brief with search findings, analyst assessment, and main conclusion sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an OpenClaw gateway token, configured main/search/analyst agents, and agent-to-agent allowlists.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
