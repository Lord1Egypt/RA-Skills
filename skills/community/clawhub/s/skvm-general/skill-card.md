## Description:

Drive the skvm CLI to profile models, AOT-compile skills, run skill-assisted tasks, run benchmarks, and manage compiled proposals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lec77](https://clawhub.ai/user/lec77)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to operate skvm for model profiling, skill compilation, benchmark runs, ad-hoc skill-assisted tasks, and compiled proposal management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill references a remote shell installer that can execute unreviewed code if run blindly.

Mitigation: Install only when skvm and its publisher are trusted; prefer a verified release, checksum, or signature validation, and review before execution.

Risk: Profiling, compilation, benchmark, and run commands can consume API keys and incur LLM usage costs.

Mitigation: Check API keys only for commands that call an LLM, and require explicit confirmation before expensive multi-model or multi-task runs.

Risk: Accepting compiled or optimized proposals can overwrite skill files.

Mitigation: Review proposal contents first and run proposal acceptance only after explicit deployment confirmation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lec77/skills/skvm-general)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May request explicit confirmation before expensive profiling or benchmarking, and before accepting proposals that modify skill files.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
