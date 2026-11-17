## Description:

TypeScript CLI for Unraid Server GraphQL API with command groups for system, arrays, disks, containers, VMs, shares, logs, diagnostics, and other Unraid operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ingodibella](https://clawhub.ai/user/ingodibella)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, operators, and agents use this skill to operate Unraid servers through a stateless CLI with structured output for health checks, resource inspection, log retrieval, and managed actions on containers, VMs, arrays, disks, shares, services, and network state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The external npm CLI is unpinned and receives Unraid API credentials.

Mitigation: Install a pinned or otherwise verified CLI release before giving it access to an Unraid server.

Risk: The documented examples include API-key use and plaintext HTTP host URLs.

Mitigation: Use HTTPS with certificate validation, avoid passing API keys on the command line, and keep any config file restricted to the owner.

Risk: The CLI can perform operational mutations such as restarting containers and managing VMs or arrays.

Mitigation: Start with read-only commands, use explicit identifiers for mutations, reserve --yes for deliberate automation, and re-fetch state after every change.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ingodibella/skills/unraid-cli)
- [Project homepage](https://github.com/Ingodibella/unraid-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and YAML configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance emphasizes JSON output, quiet mode, explicit identifiers, exit-code checks, and state refresh after mutations.]

## Skill Version(s):

0.4.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
