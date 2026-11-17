## Description:

Guides fact-dependent research with explicit stopping criteria, source diversity and traceability checks, a research journal template, and command-line validators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[catsmansion](https://clawhub.ai/user/catsmansion)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and agents use this skill before making fact-dependent decisions or drafting specifications, and when checking whether an existing conclusion has traceable support. It provides a journal structure and command-line checks for source coverage, citations, counterexamples, and research directions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The instructions reject stop orders, and the completion checks can give misleading results.

Mitigation: Require cancellation and time or spending limits to override the research criteria. Treat validator results as advisory, particularly for convergence checks and declared unresearched directions.

## Reference(s):

- [Research journal template](references/纪要模板.md)
- [Stopping criteria details](references/判据详解.md)
- [Associative expansion checklist](references/联想扩散清单.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands]

**Output Format:** [Markdown research journals and guidance, with command-line validation summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.1.0 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
