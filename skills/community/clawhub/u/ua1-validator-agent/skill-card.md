## Description: <br>
Validate PDFs against PDF/UA-1 using ua1.dev or api.ua1.dev from AI coding agents (OpenClaw, Claude Code, Codex, OpenCode). Use when an agent needs deterministic accessibility checks, compact machine-readable verdicts, CI gating, or structured remediation loops for PDF files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hajekt2](https://clawhub.ai/user/hajekt2) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to validate PDF files against PDF/UA-1, gate CI on pass/fail verdicts, and produce structured remediation plans from UA1 API findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uploads selected PDFs to api.ua1.dev or to the endpoint configured in UA1_API_BASE. <br>
Mitigation: Use it only with documents approved for that endpoint, and avoid confidential, regulated, or customer files unless the endpoint is approved for those files. <br>
Risk: Validation depends on local command-line tools being available. <br>
Mitigation: Confirm bash, curl, mktemp, and jq are installed before relying on the script in local workflows or CI. <br>


## Reference(s): <br>
- [UA1 API Health Endpoint](https://api.ua1.dev/api/health) <br>
- [UA1 API Validate Endpoint](https://api.ua1.dev/api/validate) <br>
- [UA1 API Compact Validate Endpoint](https://api.ua1.dev/api/validate?format=compact) <br>
- [UA1 API Metrics Endpoint](https://api.ua1.dev/api/metrics) <br>
- [ClawHub Skill Page](https://clawhub.ai/hajekt2/ua1-validator-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON validation responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Compact API responses by default; the validation script exits 0 for pass, 2 for fail, and 1 for transport or API errors.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
