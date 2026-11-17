## Description:

Measures OpenClaw model performance by scoring token throughput, first-token latency, tool call speed, context efficiency, and error recovery ability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhheo](https://clawhub.ai/user/zhheo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to benchmark OpenClaw agent and model performance across generation throughput, latency, tool-call speed, context efficiency, file I/O, and error recovery. It guides benchmark runs and can generate local HTML reports and baseline comparisons from metrics JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted metrics values may be rendered as HTML in generated reports.

Mitigation: Generate reports only from trusted metrics JSON, and review or escape report inputs before sharing generated HTML.

Risk: The benchmark protocol runs fixed shell commands and network tests and saves files locally.

Mitigation: Review the commands and network checks before execution, and run the benchmark only where local writes to temporary and report directories are acceptable.

Risk: Metrics, baselines, and reports can include model, provider, and system metadata.

Mitigation: Remove sensitive model, provider, or system details before sharing baseline files or generated reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhheo/skills/zhheo-openclaw-benchmark)
- [Publisher profile](https://clawhub.ai/user/zhheo)
- [Developer site](https://zhheo.com)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown instructions with bash and JSON code blocks; generated HTML benchmark reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are saved locally under the OpenClaw Benchmark results directory, with optional baseline JSON comparisons.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
