## Description:

Integrate Verosight API for social media intelligence and cyber monitoring across social, news, and web sources, including sentiment analysis, trend detection, influencer identification, bot detection, authentication setup, API querying, and report generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jrrqd](https://clawhub.ai/user/jrrqd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to connect agents to the Verosight API for social listening, digital reputation monitoring, sentiment analysis, trend tracking, influencer review, bot-pattern review, and report drafting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys and JWTs are used to authenticate with a third-party service and could be exposed if pasted into commands, logs, or reports.

Mitigation: Use test or least-privilege credentials where possible, prefer environment variables, and avoid placing production keys or JWTs directly in shared commands or generated deliverables.

Risk: Monitoring queries and returned content are sent to or retrieved from a third-party service and may involve confidential or regulated targets.

Mitigation: Submit only authorized monitoring targets and avoid confidential or regulated data unless the deployment has the required approvals and data-handling controls.

Risk: Generated client-facing reports may accidentally include internal API details, credits, keys, tokens, or raw sensitive findings.

Mitigation: Review and redact reports before distribution, especially sections derived from API metadata, account usage, or raw monitoring results.

Risk: Optional PDF report generation depends on pdfkit and local Node.js packaging.

Mitigation: Pin or isolate the optional pdfkit dependency and scan generated report code before using it in production workflows.

## Reference(s):

- [Verosight API](https://verosight.com)
- [Verosight Documentation](https://verosight.com/docs)
- [Verosight API Dashboard](https://verosight.com/dashboard)
- [Sentiment Analysis Workflow](references/sentiment-workflow.md)
- [PDF Report Generation with pdfkit](references/pdf-template.md)
- [ClawHub Skill Page](https://clawhub.ai/jrrqd/skills/verosight-monitor)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON API examples, and report templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Verosight API request examples, response interpretation guidance, and optional PDF report-generation code.]

## Skill Version(s):

1.1.2 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
