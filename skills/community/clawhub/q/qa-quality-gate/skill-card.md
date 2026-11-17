## Description:

QA lead skill for evidence review, gate enforcement, release-readiness assessment, and quality signoff recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aiweline](https://clawhub.ai/user/aiweline)

### License/Terms of Use:

MIT-0

## Use Case:

QA leads, technical leads, and engineering teams use this skill to review test evidence, enforce required quality gates, and decide whether returned work is ready for release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may produce a release recommendation from incomplete, mismatched, or weak QA evidence.

Mitigation: Require concrete test outputs, runtime logs, changed-surface mapping, and explicit missing-evidence notes before relying on a gate decision.

Risk: The skill references Weline-specific process documents, gate names, and Chinese role responsibilities that may not exist in another environment.

Mitigation: Adapt the referenced documents, validation gates, and escalation roles before using it outside the Weline workflow.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown QA gate assessment with gate-by-gate decisions, release recommendation, missing evidence, failed checks, and residual risks.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires QA strategy, implementation summary, changed surfaces, test outputs, runtime logs, and documentation evidence when relevant.]

## Skill Version(s):

1.1.0 (source: server release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
