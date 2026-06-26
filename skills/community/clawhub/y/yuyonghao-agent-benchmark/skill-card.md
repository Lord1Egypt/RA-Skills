## Description: <br>
Agent Benchmark evaluates AI agent task-completion ability across standardized file, data, system, robustness, and code-quality tasks and generates scored reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to run lightweight benchmark tasks against an AI agent, compare results across releases or configurations, and diagnose capability gaps before deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Benchmark tasks execute code directly on the host and can access local files or environment variables. <br>
Mitigation: Run the benchmark only inside a disposable sandbox, VM, or container that contains no valuable files and no secrets. <br>
Risk: Custom task files can change what code the benchmark runs. <br>
Mitigation: Review task definitions before execution and avoid untrusted custom tasks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuyonghao-123/yuyonghao-agent-benchmark) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [Test summary](artifact/TEST_SUMMARY.md) <br>
- [Optimization results](artifact/reports/optimization-results.md) <br>
- [Default task definitions](artifact/tasks/default-tasks.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON task definitions, and command-oriented setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Benchmark execution writes local report files and may run task code in the current host environment.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
