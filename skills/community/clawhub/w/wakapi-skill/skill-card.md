## Description:

Wakapi coding stats (summaries, projects, today status, totals) via a small Python CLI for Wakapi and self-hosted coding time and project or language breakdowns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chensoul](https://clawhub.ai/user/chensoul)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to query read-only Wakapi coding activity, including summaries, projects, today's status, all-time totals, and project or language breakdowns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Wakapi API key is sent in an Authorization header to the configured Wakapi instance.

Mitigation: Use an HTTPS WAKAPI_URL whenever possible and only configure instances you trust.

Risk: The configured API key can expose coding activity metadata available to that Wakapi account.

Mitigation: Use the least-privileged key available, avoid pasting WAKAPI_API_KEY into chat or shared logs, and rotate the key if it may have been exposed.

## Reference(s):

- [Wakapi API Reference](references/wakapi-api.md)
- [Wakapi Project](https://github.com/muety/wakapi)
- [Wakapi Health Route](https://github.com/muety/wakapi/blob/master/routes/api/health.go)
- [Wakapi Interval Model](https://github.com/muety/wakapi/blob/master/models/interval.go)
- [ClawHub Skill Page](https://clawhub.ai/chensoul/skills/wakapi-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI responses are JSON on stdout; HTTP/API errors are reported separately and exit non-zero.]

## Skill Version(s):

0.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
