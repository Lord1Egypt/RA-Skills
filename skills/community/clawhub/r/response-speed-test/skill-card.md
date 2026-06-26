## Description: <br>
Measures OpenClaw response timing stages and generates benchmark reports with TTFT, TPS, and total response-time metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kingofqin2026](https://clawhub.ai/user/kingofqin2026) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to benchmark local OpenClaw response stages, inspect latency across gateway, session, memory, and LLM steps, and export timing reports for comparison. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: LLM probe tests and exported reports may include prompt snippets or probe metadata. <br>
Mitigation: Avoid sensitive prompts in probe tests and review JSON or Markdown reports before sharing them. <br>
Risk: Recurring benchmark configuration can cause periodic local runs. <br>
Mitigation: Only add the HEARTBEAT.md recurring benchmark line when periodic benchmarking is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kingofqin2026/response-speed-test) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration] <br>
**Output Format:** [Console text, JSON exports, and Markdown benchmark reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may include stage timing metadata such as TTFT, TPS, total response time, and probe details.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release metadata and pyproject.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
