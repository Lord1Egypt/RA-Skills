## Description: <br>
OpenClaw smartness evaluation skill that turns local runtime state and benchmark results into structured intelligence scores, evidence, risk flags, trend analysis, and recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yh22e](https://clawhub.ai/user/yh22e) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to evaluate an OpenClaw workspace after changes, on a recurring schedule, or before sharing capability results. It produces structured scores, supporting evidence, risk flags, trend deltas, and upgrade recommendations from local tests and runtime state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local benchmark commands and reads workspace state during evaluation. <br>
Mitigation: Review config/task-suite.json before running and use the documented command validation and timeout controls. <br>
Risk: Generated reports may include summary evidence, scores, risk flags, or other workspace-derived findings. <br>
Mitigation: Redact generated JSON, Markdown, and JSONL reports before sharing them publicly. <br>
Risk: The optional LLM judge mode can send summary evaluation evidence to the configured provider. <br>
Mitigation: Avoid --llm-judge on sensitive workspaces unless sending summary evidence to that provider is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yh22e/smartness-eval-open-source) <br>
- [README](README.md) <br>
- [Architecture](docs/ARCHITECTURE.md) <br>
- [Scoring Formulas](docs/SCORING.md) <br>
- [Security Policy](SECURITY.md) <br>
- [Task Suite Configuration](config/task-suite.json) <br>
- [Rubric Configuration](config/rubrics.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands plus generated JSON, Markdown, and JSONL evaluation files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes evaluation outputs under state/smartness-eval/ and can optionally call an LLM judge only when explicitly enabled with an API key.] <br>

## Skill Version(s): <br>
0.3.3 (source: server release metadata, _meta.json, changelog released 2026-03-22) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
