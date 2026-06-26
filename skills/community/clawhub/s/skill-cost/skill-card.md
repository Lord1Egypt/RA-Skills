## Description: <br>
Track per-skill token usage and costs from OpenClaw session logs, including high-cost skills, model breakdowns, and daily breakdowns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dzwalker](https://clawhub.ai/user/dzwalker) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to inspect local session logs, identify which installed skills drive token usage and cost, and compare skill spending over time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local OpenClaw session files and installed skill metadata, which can expose sensitive usage or workflow metadata if reports are shared too broadly. <br>
Mitigation: Run it in a trusted local environment, restrict access to the OpenClaw data directory, and review generated reports before sharing them. <br>
Risk: Cost values can be approximate when session logs do not include a cost.total field and model pricing fallback data is used. <br>
Mitigation: Use the reports for skill-level triage and compare material budget decisions against provider billing or authoritative cost records. <br>


## Reference(s): <br>
- [Skill Cost on ClawHub](https://clawhub.ai/dzwalker/skill-cost) <br>
- [skill-cost repository](https://github.com/dzwalker/skill-cost) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, text, JSON, analysis] <br>
**Output Format:** [Plain text tables or JSON reports emitted by bash-wrapped Python scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports report, ranking, detail, compare, date, agent, and top-N filters.] <br>

## Skill Version(s): <br>
0.1.0 (source: SKILL.md frontmatter, claw.json, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
