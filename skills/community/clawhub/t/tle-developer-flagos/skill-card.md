## Description:

Self-contained orchestration skill for writing high-performance TLE kernels and shipping TLE feature changes with reproducible validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wbavon](https://clawhub.ai/user/wbavon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to write or optimize TLE kernels, implement TLE API/verifier/lowering/pipeline changes, and debug correctness, performance, or regression issues with reproducible validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can lead an agent to run local build scripts, editable Python installs, tests, and compiler builds from a target repository.

Mitigation: Use the skill only with trusted repositories or inside a sandbox with secrets removed.

Risk: Compiler and kernel changes can introduce correctness or performance regressions if proposed changes are accepted without validation.

Mitigation: Require the skill's validation matrix, correctness checks, benchmark records, and merge decision package before applying or shipping changes.

## Reference(s):

- [TLE Practical Guide](artifact/references/tle-sources.md)
- [Workflow and Templates](artifact/references/workflow-templates.md)
- [TLE Developer ClawHub Skill Page](https://clawhub.ai/wbavon/skills/tle-developer-flagos)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces validation commands, implementation guidance, fix summaries, lessons entries, and merge decision packages.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
