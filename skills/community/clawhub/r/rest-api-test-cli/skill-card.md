## Description:

REST API Tester helps agents test REST endpoints, validate responses, benchmark performance, debug HTTP responses, and generate HTML API test reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ericlooi504](https://clawhub.ai/user/ericlooi504)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and API engineers use this skill to exercise REST API endpoints, validate expected status codes and JSON keys, benchmark response times, test OpenAPI paths, and produce HTML reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends requests to URLs with headers and bodies supplied by the user, which can expose credentials or sensitive data to target services.

Mitigation: Use test credentials where possible, avoid production secrets, confirm target URLs before execution, and be cautious with redirects.

Risk: Generated HTML reports may include untrusted API response content and sensitive request or response data.

Mitigation: Do not open or share reports from untrusted endpoints until escaping and redaction are confirmed, and review generated reports before distribution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ericlooi504/skills/rest-api-test-cli)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands and generated HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can emit console summaries, validation results, benchmark statistics, and local HTML reports.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
