## Description: <br>
Benchmark sglang serving performance on AMD Instinct GPUs (MI355X, MI300X, MI308X) with TP, DP, and EP parallel configurations, throughput and latency sweeps, TTFT/TPOT measurement, and mix-mode configuration comparison. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexsun07](https://clawhub.ai/user/alexsun07) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and performance engineers use this skill to plan and run SGLang LLM serving benchmarks on AMD Instinct GPU hosts. It helps compare TP, DP, and EP configurations, collect throughput and latency metrics, and produce benchmark artifacts for configuration-level analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence says the skill automatically enables model-supplied code execution. <br>
Mitigation: Install and run it only on a dedicated GPU host or isolated container, use trusted pinned model files, and avoid unreviewed Hugging Face model repositories. <br>
Risk: Additional launch flags can materially change benchmark server behavior. <br>
Mitigation: Inspect the DRY_RUN output before launching and review any EXTRA_ARGS before execution. <br>
Risk: Server lifecycle commands can affect running SGLang processes on shared systems. <br>
Mitigation: Use stop.sh only in the intended container or host context and verify released GPU processes before starting the next benchmark. <br>


## Reference(s): <br>
- [SGLang server configuration and parallel strategy](references/server_config.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and benchmark artifact files such as JSONL, CSV, and PNG outputs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces benchmark planning guidance, launch commands, server logs, JSONL metrics, converted CSV data, and optional interactivity plots.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
