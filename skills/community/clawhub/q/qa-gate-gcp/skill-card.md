## Description:

Pre-production validation gate for GCP stacks that generates test plans, executes automated checks across APIs, UI flows, authentication, LLM quality, databases, and cloud infrastructure, and produces go/no-go reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guifav](https://clawhub.ai/user/guifav)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, and release engineers use this skill to run a pre-production validation gate for GCP applications. It helps plan and execute checks for APIs, UI and toast behavior, auth flows, LLM-powered features, Firestore, Cloud SQL, Secret Manager, and Cloud Run before producing a go/no-go report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and model outputs can be sent to OpenRouter during LLM-as-judge checks.

Mitigation: Use synthetic or approved test data, redact sensitive content, and run LLM judging only when OpenRouter processing is approved by the organization.

Risk: Validation commands run in a GCP/testing environment with credentials and broad read access.

Mitigation: Run the skill in isolated pre-production workspaces with least-privilege IAM and review generated commands before execution.

Risk: Generated reports and logs may contain environment details from test execution.

Mitigation: Review and redact reports before sharing, and keep secret values out of logs and artifacts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guifav/skills/qa-gate-gcp)
- [OpenRouter chat completions endpoint](https://openrouter.ai/api/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with JSON plans, generated test code and scripts, shell commands, and JSON or Markdown go/no-go reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate qa-tests/ and qa-reports/ files when applied by an agent.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
