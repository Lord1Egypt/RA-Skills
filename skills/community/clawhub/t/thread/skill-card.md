## Description:

Provides guidance and code examples for using threads, synchronization, thread pools, and concurrency patterns across languages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlang-cn](https://clawhub.ai/user/openlang-cn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to choose between threads, processes, and async approaches, and to generate or review concurrency examples involving locks, queues, thread pools, race conditions, and deadlock avoidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The README is Chinese-only, which may make human review harder for non-Chinese readers.

Mitigation: Review SKILL.md and the English reference files directly, or translate README.md before release approval.

Risk: Broad activation wording can cause the skill to appear for general concurrency questions.

Mitigation: Confirm that broad activation is acceptable for the target agent, or narrow the activation phrasing before deployment.

Risk: Concurrency guidance or generated code can introduce races, deadlocks, or inefficient thread usage if copied without review.

Mitigation: Review generated code for synchronization, lock ordering, queue usage, and runtime-specific limits such as Python's GIL before production use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/openlang-cn/skills/thread)
- [Thread Reference](reference/README.md)
- [Thread vs Process vs Async](reference/concepts.md)
- [Concurrency Patterns](reference/patterns.md)
- [Language Quick Reference](reference/languages.md)
- [Thread Assets](assets/README.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code]

**Output Format:** [Markdown with inline code examples and optional code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May adapt bundled Python threading and ThreadPoolExecutor templates when requested.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
