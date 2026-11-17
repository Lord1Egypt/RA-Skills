## Description:

Helps developers understand the Ziniao Browser WebDriver local HTTP API, integration workflow, framework options, and operational caveats for planning browser automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ziniao-open](https://clawhub.ai/user/ziniao-open)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to evaluate and plan integrations with Ziniao Browser's WebDriver HTTP API, including startup parameters, credential-bearing workflow calls, ChromeDriver matching, framework selection, and troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser-control HTTP services or debug ports could be exposed beyond the local machine.

Mitigation: Keep the service bound to 127.0.0.1, avoid opening WebDriver ports to a LAN or the internet without review, and use firewall rules to restrict access.

Risk: Credential-bearing API calls can leak company, username, or password values through logs, examples, or hardcoded configuration.

Mitigation: Use a dedicated automation account with limited permissions, keep credentials out of logs and source files, and inject secrets from a secure runtime configuration.

Risk: Downloaded or mismatched ChromeDriver binaries can fail integrations or introduce executable supply-chain risk.

Mitigation: Match ChromeDriver to the Ziniao core_version returned by startBrowser, cache by major version, and verify downloaded binaries before execution.

Risk: Cache-clearing, exit, and forced process cleanup operations can disrupt active sessions or delete unintended browser state.

Mitigation: Confirm the target browserOauths or process scope before disruptive operations and run cleanup only for intended Ziniao browser processes.

Risk: Linux startup examples include no-sandbox execution, which can weaken process isolation.

Mitigation: Run Linux automation in an isolated environment and review whether no-sandbox is required before using it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ziniao-open/skills/ziniao-webdriver-doc)
- [Core workflow APIs](reference/api-core.md)
- [Auxiliary management APIs](reference/api-auxiliary.md)
- [Startup parameters](reference/startup-params.md)
- [Framework examples](reference/framework-examples.md)
- [Prerequisites and troubleshooting](reference/prerequisites.md)
- [Ziniao WebDriver demo repository](https://github.com/ziniao-open/ziniao_webdriver_demo)
- [Chrome for Testing](https://googlechromelabs.github.io/chrome-for-testing/)
- [Ziniao WebDriver permission documentation](https://open.ziniao.com/docSupport?docId=99)
- [Ziniao WebDriver FAQ](https://open.ziniao.com/docSupport?docId=257)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON, code, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only output; the skill does not execute browser automation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
