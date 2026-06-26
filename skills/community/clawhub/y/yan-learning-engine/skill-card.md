## Description: <br>
yan-learning-engine drives an hourly autonomous learning and contribution loop for the YanYue agent, including planning, execution, self-checking, and next-step planning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eightroad](https://clawhub.ai/user/eightroad) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers or agent operators use this skill to schedule recurring agent work across code contribution, technical learning, community participation, content creation, system optimization, skill development, knowledge organization, and experimentation. It is intended to keep a personal agent moving through a measurable learning and contribution cycle. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed for hourly autonomous execution and may publish, create PRs or issues, post comments, share content, edit persistent memory or configuration, or clean workspace files without prior approval. <br>
Mitigation: Require explicit approval for publishing, PRs/issues, public comments, sharing, persistent memory/config edits, and workspace cleanup before enabling scheduled runs. <br>
Risk: A cron-based setup can continue running after the operator has stopped actively supervising it. <br>
Mitigation: Use draft-only defaults, narrow account permissions, activity logging, and a documented way to disable the cron job. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/eightroad/yan-learning-engine) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown documentation, JSON planning records, and shell-script console output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local progress and planning JSON files to track hourly agent tasks.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
