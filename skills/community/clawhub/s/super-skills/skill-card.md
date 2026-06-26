## Description: <br>
Decomposes complex user requests into executable subtasks, identifies required capabilities, searches for existing skills at skills.sh, and creates new skills when no solution exists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[10e9928a](https://clawhub.ai/user/10e9928a) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to break complex multi-step requests into executable subtasks, identify required capabilities, find existing skills, and plan new skill creation when gaps remain. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expand an agent's capabilities by finding, creating, or installing other skills with weak review boundaries. <br>
Mitigation: Require human review and security scanning for every discovered or generated skill before installation or use. <br>
Risk: Auto-confirmed global installs can make unreviewed skills available beyond the immediate task. <br>
Mitigation: Avoid `-g -y` auto-confirm global installs; prefer trusted, pinned sources and explicit approval for installation scope. <br>
Risk: Generated plans may involve credentials, scheduled jobs, or external service changes. <br>
Mitigation: Require explicit confirmation before handling credentials, configuring scheduled execution, or modifying external services. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/10e9928a/super-skills) <br>
- [Skills ecosystem](https://skills.sh/) <br>
- [Capability types reference](references/capability_types.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with structured task breakdowns and inline command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include skill search recommendations, skill creation plans, execution steps, and security review guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
