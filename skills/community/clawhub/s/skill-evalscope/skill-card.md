## Description:

EvalScope helps agents translate model evaluation, performance testing, RAG evaluation, benchmark discovery, and result-visualization requests into EvalScope CLI commands and configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yunnglin](https://clawhub.ai/user/yunnglin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan and run EvalScope workflows for LLM accuracy benchmarks, inference performance tests, RAG quality checks, benchmark lookup, and result inspection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Evaluation commands can expose API keys, prompts, datasets, model outputs, or judge inputs through shell history, logs, dashboards, and generated reports.

Mitigation: Use redacted or local data for confidential evaluations, avoid placing real API keys directly in command lines, and review generated outputs before sharing them.

Risk: Broad optional installs, dashboard exposure, and Docker sandbox benchmarks can increase the local execution or data exposure surface.

Mitigation: Use a virtual environment or container, pin package versions where possible, install only the needed EvalScope extras, keep dashboards bound to localhost unless intentionally exposed, and be cautious with Docker benchmarks on machines that hold sensitive files or credentials.

## Reference(s):

- [Eval Parameter Reference](eval-reference.md)
- [Perf Parameter Reference](perf-reference.md)
- [RAG Evaluation Reference](rag-reference.md)
- [Examples](examples.md)
- [Troubleshooting](troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, Python configuration snippets, and troubleshooting guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose EvalScope commands that call local tools, APIs, dashboards, Docker sandboxes, or model evaluation backends.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
