## Description: <br>
Connect OpenClaw to TestDino for real-time Playwright CI intelligence. Ask about test failures, flaky tests, run history, and CI health in plain English. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[testdino-inc](https://clawhub.ai/user/testdino-inc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and QA engineers use this skill to query TestDino from OpenClaw for Playwright CI failures, flaky tests, run history, branch merge readiness, failure alerts, and scheduled test health digests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a TestDino Personal Access Token and can expose CI metadata through configured assistant or notification workflows. <br>
Mitigation: Use the least-privileged token available, keep the token out of shared files and commits, and restrict local configuration file permissions. <br>
Risk: The skill relies on approved local command execution through mcporter and npm-installed MCP packages. <br>
Mitigation: Install only if the mcporter and testdino-mcp packages are trusted, and review commands before enabling the skill. <br>
Risk: Cron examples can send CI results to external channels such as Slack, Discord, Telegram, or WhatsApp. <br>
Mitigation: Review scheduled jobs, destination channels, and message contents before enabling automated alerts or digests. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/testdino-inc/testdino-playwright) <br>
- [OpenClaw](https://openclaw.dev) <br>
- [TestDino application](https://app.testdino.com) <br>
- [mcporter npm package](https://www.npmjs.com/package/mcporter) <br>
- [testdino-mcp npm package](https://www.npmjs.com/package/testdino-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, API Calls] <br>
**Output Format:** [Markdown guidance with shell commands and concise CI summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires mcporter, testdino-mcp, and a TESTDINO_PAT credential; responses should use only fields returned by the TestDino tools.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
