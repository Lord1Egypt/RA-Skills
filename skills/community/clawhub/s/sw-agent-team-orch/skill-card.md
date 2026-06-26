## Description: <br>
Set up and coordinate multi-agent teams with defined roles, task workflows, handoff protocols, and quality review checkpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amdf01-debug](https://clawhub.ai/user/amdf01-debug) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to design multi-agent workflows, assign clear specialist roles, define handoff briefs, and set review gates before delivering work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Handoff briefs or shared state files may accidentally include secrets, private credentials, or sensitive project context. <br>
Mitigation: Keep shared state inside the relevant project, avoid writing secrets into briefs, and review persistent context before another agent reuses it. <br>
Risk: Coordinated agents may propagate incorrect assumptions or unverified information across tasks. <br>
Mitigation: Use explicit acceptance criteria, require review checkpoints, and verify links, references, and factual claims before delivery. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/amdf01-debug/sw-agent-team-orch) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown templates and structured planning guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No executable code; produces coordination plans, handoff formats, and quality-gate checklists.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
