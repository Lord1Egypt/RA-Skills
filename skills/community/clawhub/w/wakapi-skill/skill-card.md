## Description: <br>
Wakapi Query provides read-only Wakapi coding statistics for summaries, projects, status bar, totals, and health checks through a small Python CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chensoul](https://clawhub.ai/user/chensoul) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to query a Wakapi instance for read-only coding-time summaries, project and language breakdowns, today's status line, all-time totals, and health status. It is useful when a user has configured WAKAPI_URL and, for authenticated commands, WAKAPI_API_KEY. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated commands use WAKAPI_API_KEY to access coding-time statistics from the configured Wakapi instance. <br>
Mitigation: Keep the API key in the environment, avoid pasting it into chat or logs, and use a least-privilege or revocable key where the Wakapi deployment supports it. <br>
Risk: The skill sends outbound requests to WAKAPI_URL, so a misconfigured URL can disclose request timing or queries to the wrong service. <br>
Mitigation: Verify WAKAPI_URL before running commands and prefer HTTPS for deployed Wakapi instances. <br>


## Reference(s): <br>
- [Wakapi API Reference](artifact/references/wakapi-api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/chensoul/wakapi-skill) <br>
- [Wakapi Query Repository](https://github.com/chensoul/wakapi-skill) <br>
- [Wakapi Project](https://github.com/muety/wakapi) <br>
- [Wakapi Health Route](https://github.com/muety/wakapi/blob/master/routes/api/health.go) <br>
- [Wakapi Interval Model](https://github.com/muety/wakapi/blob/master/models/interval.go) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python CLI commands and JSON API output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The CLI reads WAKAPI_URL for all commands and WAKAPI_API_KEY for authenticated commands; health checks do not use the API key.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
