## Description:

Helps agent users, skill authors, maintainers, and teams turn Multi Search Engine-style workflow needs into practical artifacts, checklists, analysis, code changes, or decision support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

External agent users, skill authors, maintainers, and teams use this skill to clarify productivity and multi-search workflow requests, produce concrete implementation or planning artifacts, and validate the result against visible success criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate for ordinary search or workflow requests because its trigger wording is broad.

Mitigation: Narrow trigger terms or require explicit invocation where precise routing matters.

Risk: Workflow guidance, generated scripts, or configuration suggestions may be incorrect for a user's local environment.

Mitigation: Review outputs before use and validate them against the user's stated success criteria and constraints.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/work-productivity-multi-search-workflow-helper-102347)
- [Popular ClawHub skill demand: Multi Search Engine](https://clawhub.ai/skills/multi-search-engine)
- [Hacker News: Seeking Advice](https://news.ycombinator.com/item?id=48621795)
- [SegmentFault: javascript](https://segmentfault.com/t/javascript)
- [SegmentFault: typescript](https://segmentfault.com/t/typescript)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with optional code blocks, shell commands, checklists, templates, and validation notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be tailored to the user's stated constraints and should include assumptions, limits, and a short verification note when helpful.]

## Skill Version(s):

0.20260729.110214 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
