## Description:

Designs email A/B, multivariate, send-time, and hold-out experiments and reads finished ESP results for effect size, uncertainty, statistical significance, practical materiality, and guardrails without choosing a business action on its own.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing operators, lifecycle teams, and analysts use this skill to design controlled email experiments, plan sample size and duration, and read completed campaign results with documented uncertainty and guardrails. It is intended for experiment planning and interpretation, not for writing email creative or making the final business decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process email performance, conversion, and revenue data supplied by the user.

Mitigation: Use manual exports or scoped ESP access where possible, and avoid providing data that is not needed for the experiment design or read-out.

Risk: Saved memory can preserve summarized experiment context for future sessions.

Mitigation: Approve memory saving only when the summarized context is appropriate to retain.

Risk: Statistical output could be mistaken for an automatic business decision.

Mitigation: Require a named owner and precommitted action rule; otherwise keep the result at decision: UNDECIDED.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aaron-he-zhu/skills/send-experiment-designer)
- [Project homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown test-design or read-out document with optional inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a Handoff Summary, calculated effect and uncertainty fields, guardrail status, and decision: UNDECIDED when no owner-approved action rule exists.]

## Skill Version(s):

19.0.0 (source: evidence release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
