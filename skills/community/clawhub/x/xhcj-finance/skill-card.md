## Description:

Queries Xinhua Finance market quotes, K-line data, stock symbol matches, and finance news through a command-line interface.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jindongyi011039](https://clawhub.ai/user/jindongyi011039)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to run a Node.js CLI for Xinhua Finance data lookups, including market data, K-line data, stock symbol search, and categorized finance news.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI requires an API key to be passed as a command-line option, which can expose credentials in shell history, shared scripts, logs, or CI output.

Mitigation: Use a dedicated low-privilege key, avoid committing or logging commands that contain real keys, and prefer a reviewed release with improved credential handling before broad deployment.

Risk: The package has dependency-hardening gaps and no lockfile in the artifact.

Mitigation: Install in a controlled environment, pin and review dependency versions, and scan the resolved dependency tree before production use.

Risk: The skill sends requests to the documented Xinhua Finance endpoint for Chinese-market finance data.

Mitigation: Use only in environments where this network destination and data source are acceptable for the organization and use case.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jindongyi011039/skills/xhcj-finance)
- [ClawHub publisher profile](https://clawhub.ai/user/jindongyi011039)
- [Xinhua Finance OpenClaw endpoint](https://xhcj-h5-zg.cnfin.com/xhcj-bun/func/openclaw)

## Skill Output:

**Output Type(s):** [Shell commands, Text, JSON]

**Output Format:** [Plain text CLI output with JSON-formatted response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Xinhua Finance API key supplied on the command line.]

## Skill Version(s):

1.0.8 (source: frontmatter, package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
