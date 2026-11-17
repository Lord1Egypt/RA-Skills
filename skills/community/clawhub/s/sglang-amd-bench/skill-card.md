## Description:

Benchmark SGLang serving performance on AMD Instinct GPUs (MI355X, MI300X, MI308X) across TP, DP, and EP parallel configurations, throughput and latency sweeps, TTFT/TPOT measurement, and mix-mode configuration comparison.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexsun07](https://clawhub.ai/user/alexsun07)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and performance engineers use this skill to plan and run SGLang benchmark sweeps on AMD Instinct GPU hosts, compare parallel serving configurations, and produce benchmark logs, CSV data, plots, and a Markdown performance report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can execute model-supplied code because the SGLang launcher always enables remote model code execution.

Mitigation: Use only trusted model repositories or local model files, keep model downloads disabled, and review model code before running benchmarks.

Risk: The bundled stop script can force-kill broad SGLang processes, which is risky on shared GPU hosts.

Mitigation: Confirm the target processes before stopping servers on shared hosts, or replace broad cleanup with PID-scoped shutdown for managed environments.

## Reference(s):

- [SGLang Server Configuration & Parallel Strategy](references/server_config.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands, generated benchmark logs, JSONL results, CSV summaries, plots, and a Markdown report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces mix-mode SGLang benchmark artifacts under the selected workspace and relies on explicit user confirmation before execution.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
