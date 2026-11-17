## Description:

Choose the best OpenClaw skill by matching trigger keywords to the TOOLS.md index, then applying strict judgment rules (most specific first; if in doubt, use it).

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuchang9337-dev](https://clawhub.ai/user/xuchang9337-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent maintainers use this skill to choose an appropriate OpenClaw skill or skill combination from a TOOLS.md index, especially when multiple candidate skills match a request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages invoking a candidate skill when the fit is unclear.

Mitigation: Use an orchestrator policy that requires confirmation or a fail-closed path for ambiguous, sensitive, or side-effecting requests.

Risk: A wrong TOOLS.md mapping can route the agent to an unsuitable skill.

Mitigation: Review and maintain the skill index so trigger keywords, summaries, and callable skill identifiers remain accurate.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xuchang9337-dev/skills/skill-invocation)
- [Publisher Profile](https://clawhub.ai/user/xuchang9337-dev)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text decision guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include selected skill identifiers, a short reason, and a recommended next action.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
