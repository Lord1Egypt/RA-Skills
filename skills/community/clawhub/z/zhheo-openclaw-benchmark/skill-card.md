## Description: <br>
Measures OpenClaw model performance by scoring token throughput, first-token latency, tool call speed, context efficiency, and error recovery ability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhheo](https://clawhub.ai/user/zhheo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to run local OpenClaw benchmark tasks, compute a composite performance score, and generate reports comparing model speed, tool latency, context efficiency, and recovery behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The benchmark runs local shell commands and writes metrics or reports to /tmp and ~/Downloads/OpenClaw-Benchmark. <br>
Mitigation: Review the benchmark commands before running and delete /tmp/bench_metrics.json or ~/Downloads/OpenClaw-Benchmark when local benchmark history should not be retained. <br>
Risk: Generated reports can reflect values from metrics JSON. <br>
Mitigation: Open only reports generated from trusted metrics JSON. <br>
Risk: Some benchmark steps make outbound web requests. <br>
Mitigation: Run those steps only in an environment where simple outbound benchmark requests are acceptable. <br>


## Reference(s): <br>
- [OpenClaw Benchmark ClawHub page](https://clawhub.ai/zhheo/zhheo-openclaw-benchmark) <br>
- [zhheo publisher profile](https://clawhub.ai/user/zhheo) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Shell commands, Configuration instructions, Files] <br>
**Output Format:** [Markdown instructions with shell commands, JSON metrics, and HTML benchmark reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local report files under ~/Downloads/OpenClaw-Benchmark/results and optional baseline JSON files.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
