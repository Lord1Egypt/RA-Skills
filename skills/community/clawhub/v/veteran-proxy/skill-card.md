## Description:

Guides agents in managing the Veteran proxy client, including subscription updates, node listing, local SOCKS5 proxy start and stop commands, status checks, and split-routing rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[veteran-cli](https://clawhub.ai/user/veteran-cli)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and external users use this skill to configure and troubleshoot the Veteran CLI when they need proxy access to network resources. It covers subscription setup, node selection, local proxy lifecycle commands, browser proxy settings, and split-routing rule configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install and run a mutable third-party proxy client.

Mitigation: Review the package source before installing, prefer pinned or verified installs, and avoid unreviewed global or npx execution in sensitive environments.

Risk: Proxy subscription URLs may expose sensitive access information if placed in shared commands, shell history, or logs.

Mitigation: Use trusted subscription providers, avoid real subscription URLs in reusable examples or shared logs, and handle VETERAN_SUB_URL as sensitive configuration.

Risk: Starting a local proxy can redirect application traffic in ways users may not expect.

Mitigation: Confirm which applications use 127.0.0.1 proxy settings, review split-routing rules before enabling them, and verify the stop command before starting background proxy instances.

## Reference(s):

- [Veteran Proxy ClawHub listing](https://clawhub.ai/veteran-cli/skills/veteran-proxy)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local proxy addresses, port numbers, environment variables, and routing-rule examples.]

## Skill Version(s):

1.0.2 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
