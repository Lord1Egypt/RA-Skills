## Description: <br>
Pre-production validation gate for GCP stack (Cloud Run/Functions/App Engine, Firestore/Cloud SQL, Firebase Auth/Identity Platform) that generates test plans, executes test suites, validates APIs, UI, toasts, LLM output quality, and produces go/no-go reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guifav](https://clawhub.ai/user/guifav) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and QA engineers use this skill as a pre-production validation gate for GCP applications. It plans and runs validation across APIs, UI flows, authentication, LLM output quality, databases, and GCP infrastructure before producing go/no-go reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run tests and generated scripts against GCP resources, which may affect production-like systems if pointed at the wrong project. <br>
Mitigation: Use only staging, disposable, or isolated GCP environments and review generated scripts before execution. <br>
Risk: GCP credentials and service accounts are required for infrastructure validation. <br>
Mitigation: Use least-privilege service accounts, avoid production data, and keep validation commands read-only. <br>
Risk: LLM-as-judge evaluations may send prompts and outputs to OpenRouter or upstream model providers. <br>
Mitigation: Avoid sensitive data in LLM evaluation samples and review provider data-handling requirements before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guifav/qa-gate-gcp) <br>
- [OpenRouter Chat Completions API endpoint](https://openrouter.ai/api/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON plans, generated test code, shell commands, validation logs, and JSON/Markdown reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces qa-reports/test-plan.json, qa-reports/go-no-go-report.json, qa-reports/go-no-go-report.md, and generated validation scripts under qa-tests/.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
