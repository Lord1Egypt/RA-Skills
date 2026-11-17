## Description:

Remote Terminal helps agents connect to remote Linux servers, run commands over SSH, manage host records, and coordinate multi-host operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckaorceu](https://clawhub.ai/user/ckaorceu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect and manage remote Linux servers through SSH commands, host configuration guidance, and optional parallel execution across multiple hosts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run powerful SSH commands on remote servers, including production systems.

Mitigation: Install only when users are comfortable granting remote command authority; review commands and target hosts before execution.

Risk: Credential handling creates exposure if passwords are passed directly or stored in host configuration.

Mitigation: Prefer SSH keys with an agent, avoid password options, and do not store passwords in hosts.json.

Risk: Parallel execution can affect many machines at once.

Mitigation: Review host files before use, limit target groups, and test commands on a low-risk host before fleet-wide execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ckaorceu/skills/remote-terminal)
- [Security Best Practices for Remote Terminal Access](references/security_best_practices.md)
- [SSH Config Guide](references/ssh_config_guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, configuration snippets, and command output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include stdout, stderr, exit codes, timing, host details, and safety confirmations for dangerous commands.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
