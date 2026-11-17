## Description:

Creates, edits, evaluates, benchmarks, and optimizes agent skills through guided drafting, test runs, review workflows, and description tuning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wm-zqbx](https://clawhub.ai/user/wm-zqbx)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and skill authors use this skill to create new agent skills, improve existing skills, run qualitative and quantitative evaluations, review results, and optimize skill descriptions for better triggering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local review server can stop unrelated local processes or expose or corrupt review data.

Mitigation: Review or patch the viewer before use, remove automatic port killing, and prefer static output or a short-lived foreground server for sensitive evaluation outputs.

Risk: Generated review pages may include untrusted evaluation outputs and third-party CDN resources.

Mitigation: Avoid third-party CDN resources and do not open generated review pages containing untrusted outputs until script-embedding concerns are fixed.

Risk: The skill runs local Python tools, launches Claude CLI subprocesses, creates evaluation files, and opens a local review UI.

Mitigation: Install only when this local execution behavior is acceptable, and review generated files and commands before deployment.

## Reference(s):

- [Evaluation and Benchmark Schemas](references/schemas.md)
- [ClawHub Skill Page](https://clawhub.ai/wm-zqbx/skills/skill-creator-ming)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON examples, shell commands, generated skill files, evaluation artifacts, and review reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local files for skills, evaluations, benchmark summaries, and review UI output.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
