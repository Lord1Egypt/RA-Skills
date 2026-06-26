## Description: <br>
Skill Perf benchmarks OpenClaw skills by running calibration and test subagents, subtracting measured baseline token use, and producing token and performance summaries with HTML reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kincaidwoo](https://clawhub.ai/user/kincaidwoo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to measure token consumption and performance overhead for OpenClaw skills before release, comparison, or optimization. It is intended for controlled benchmark tasks that can safely be executed by subagents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Benchmark tasks execute target skills for real and can consume model tokens or trigger side effects from the skill under test. <br>
Mitigation: Use harmless test prompts and avoid destructive, account-changing, or externally visible workflows unless separate safeguards are in place. <br>
Risk: The skill reads detailed local OpenClaw session and transcript artifacts while building measurements and reports. <br>
Mitigation: Avoid secrets, customer data, and sensitive prompts in benchmark runs; review local reports and stored results before sharing. <br>
Risk: Generated HTML reports are automatically served from a local report server. <br>
Mitigation: Treat the report URL as local diagnostic output and review report contents before exposing them outside the machine. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kincaidwoo/skill-perf) <br>
- [kincaidwoo Publisher Profile](https://clawhub.ai/user/kincaidwoo) <br>
- [Token Guide](references/TOKEN_GUIDE.md) <br>
- [Subagent Architecture Spec](docs/subagent-architecture-spec.md) <br>
- [Bugfix Notes](docs/2026-03-27-bugfix-notes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, HTML report, guidance] <br>
**Output Format:** [Markdown summary with shell command snippets and a generated local HTML report link] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include measured baseline noise, test total tokens, net token consumption, confidence rating, and local report URL when generated.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
