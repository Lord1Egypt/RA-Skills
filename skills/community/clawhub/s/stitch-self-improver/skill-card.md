## Description: <br>
Helps an AI agent learn from mistakes, optimize repeated work, and record lessons over time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdt328606](https://clawhub.ai/user/sdt328606) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to guide an AI agent in documenting mistakes, identifying recurring error patterns, and maintaining useful long-term workflow notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to keep persistent behavioral memory, which can capture sensitive personal or business details if boundaries are unclear. <br>
Mitigation: Set explicit rules for what may be stored, require confirmation before writing preferences or long-term memory, and avoid recording sensitive details. <br>
Risk: The skill directs preference changes to be shared with another agent, which can spread unreviewed or unwanted profile changes. <br>
Mitigation: Disable automatic cross-agent sharing unless the user deliberately approves the specific update. <br>
Risk: Recurring error patterns can be promoted into durable rules that may encode mistaken conclusions. <br>
Mitigation: Review proposed MEMORY, SOUL, TOOLS, and skill updates before accepting them, and archive obsolete notes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdt328606/stitch-self-improver) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/sdt328606) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown guidance and structured notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose persistent memory, lesson, tool, and skill-rule updates when the host agent permits those changes.] <br>

## Skill Version(s): <br>
2.0.0 (source: SKILL.md frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
