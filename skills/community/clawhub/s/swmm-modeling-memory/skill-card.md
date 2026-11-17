## Description:

Summarizes historical Agentic SWMM audit artifacts into reusable modeling memory, lessons learned, failure patterns, and human-reviewed skill update proposals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhonghao1995](https://clawhub.ai/user/zhonghao1995)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill after SWMM experiment audits to summarize repeated assumptions, QA issues, failures, missing evidence, run-to-run differences, and proposed skill refinements across audited runs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted run notes or audit artifacts could introduce misleading content into generated modeling memory used by an agent.

Mitigation: Use trusted or reviewed run directories and review generated Markdown before using it for retrieval or accepting any proposed skill update.

Risk: Memory refresh can mutate run-level or aggregate memory files when a user only wants analysis.

Mitigation: Keep --runs-dir and --out-dir narrowly scoped, and disable per-run or audit-end memory refresh when mutation is unwanted.

## Reference(s):

- [Agentic SWMM Project](https://github.com/Zhonghao1995/agentic-swmm-workflow)
- [SWMM Modeling Memory Example](examples/README.md)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Guidance]

**Output Format:** [JSON and Markdown files with human-readable summaries and reviewable proposals]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes aggregate memory outputs under the selected output directory and can optionally write run-level memory summaries and Obsidian-compatible Markdown.]

## Skill Version(s):

0.7.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
