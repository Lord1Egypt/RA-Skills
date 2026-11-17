## Description:

Consolidate Agentic SWMM run artifacts into auditable provenance, comparison records, and local Obsidian audit notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhonghao1995](https://clawhub.ai/user/zhonghao1995)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill after Agentic SWMM build, run, or QA attempts to consolidate manifests, logs, metrics, artifact paths, QA checks, and optional run-to-run comparisons into auditable records for reproducibility and review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Direct script mode can write audit notes outside the run directory to a local Obsidian vault by default.

Mitigation: Use the canonical aiswmm audit command without --obsidian, or pass --no-obsidian to the direct script, unless vault updates are explicitly intended.

Risk: The audit script can execute adjacent repository helper modules when certain water-quality or uncertainty artifacts are present.

Mitigation: Run the skill only in a trusted Agentic SWMM repository and inspect adjacent helper code before auditing untrusted artifacts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhonghao1995/skills/swmm-experiment-audit)
- [Agentic SWMM project](https://github.com/Zhonghao1995/agentic-swmm-workflow)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown notes, JSON audit records, and CLI command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes experiment_provenance.json, experiment_note.md, model_diagnostics.json, and comparison.json under a run audit directory; direct script mode can also copy notes to a local Obsidian vault unless disabled.]

## Skill Version(s):

0.7.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
