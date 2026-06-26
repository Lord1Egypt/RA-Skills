## Description: <br>
Use when the user starts a new multi-step task, asks to pick/install/manage skills, tune skill performance, or fire/remove a skill after failure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thinkitpossible](https://clawhub.ai/user/thinkitpossible) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to turn a user task into a job description, match or recruit an appropriate installed skill, hand off work, and record performance outcomes for later routing decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can influence which other skills are selected or installed. <br>
Mitigation: Review recruitment recommendations and require explicit approval before installs, package installers, submodules, or downloaded scripts are run. <br>
Risk: The skill writes local HR-style records under .skill-hr/. <br>
Mitigation: Keep secrets out of incidents and review registry or incident records before committing or sharing a workspace. <br>
Risk: The skill can recommend removing skills from the eligible pool and may discuss physical uninstall paths. <br>
Mitigation: Prefer registry termination for routing changes and require explicit confirmation plus path review before deleting skill directories. <br>


## Reference(s): <br>
- [Skill HR source](SKILL.md) <br>
- [Competency model and vetoes](references/01-competency-model.md) <br>
- [Job description specification](references/02-jd-spec.md) <br>
- [Matching rubric](references/03-matching-rubric.md) <br>
- [Market recruitment](references/04-market-recruitment.md) <br>
- [Performance, probation, and termination](references/05-performance-and-termination.md) <br>
- [State and artifacts](references/06-state-and-artifacts.md) <br>
- [OpenClaw host adapter](references/hosts/openclaw.md) <br>
- [Claude Code host adapter](references/hosts/claude-code.md) <br>
- [P02 output schema](schemas/p02-output.schema.json) <br>
- [Matching benchmark metrics](benchmarks/matching/METRICS.md) <br>
- [ClawHub skill page](https://clawhub.ai/thinkitpossible/skill-hr) <br>
- [Claude Code documentation](https://docs.anthropic.com/claude-code) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with structured JSON artifacts and occasional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update project-local .skill-hr registry and incident files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
