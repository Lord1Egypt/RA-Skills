## Description:

Performs systematic technical-domain research and produces structured Markdown reports covering concept analysis, industry intelligence, solution comparison, essence integration, and final consolidation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linshengli](https://clawhub.ai/user/linshengli)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to research a technical field for technology selection, domain onboarding, competitive analysis, or internal knowledge sharing. It guides the agent to gather current web evidence and organize findings into reusable Markdown reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs live web research, so results may include stale, incomplete, or low-quality external sources.

Mitigation: Review cited sources, dates, and selection rationale before relying on the generated research for decisions.

Risk: The skill creates multiple Markdown files in a research/{topic}/ directory, which may collide with existing topic files.

Mitigation: Run it in a workspace where generated research files are acceptable and check for existing files with the same topic name before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linshengli/skills/technical-research)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown reports with tables, code blocks, diagrams, citations, and summary sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes multiple topic-scoped Markdown files under research/{topic}/ and expects live web research for current project, paper, and blog data.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
