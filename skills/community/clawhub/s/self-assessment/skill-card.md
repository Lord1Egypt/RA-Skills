## Description:

Provides an agent self-assessment protocol for deciding whether to accept a task, accept with caveats, or recommend reassignment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evianevans](https://clawhub.ai/user/evianevans)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and multi-agent system operators use this skill before task acceptance to evaluate capability fit, relevant experience, skill gaps, and whether another agent should handle the work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read agent memory, logs, local skill directories, and identity files during self-assessment.

Mitigation: Install and run it only in environments where that local review is intended and where access to persistent agent state is controlled.

Risk: The skill may install additional skills and rewrite persistent identity or preference files.

Mitigation: Review proposed installations and persistent file changes before allowing them in shared or production agent environments.

## Reference(s):

- [Self Assessment skill page](https://clawhub.ai/evianevans/skills/self-assessment)
- [evianevans publisher profile](https://clawhub.ai/user/evianevans)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with structured decision blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs one of ACCEPT, ACCEPT_WITH_CAVEAT, or SUGGEST_REASSIGN, with optional SKILL_GAP guidance.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
