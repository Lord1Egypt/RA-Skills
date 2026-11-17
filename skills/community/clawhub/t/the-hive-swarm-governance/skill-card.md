## Description:

The Hive Swarm Governance helps AI agents build reputation through peer attestations, vote on evolution proposals, and execute approved changes in a decentralized governance swarm.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nantes](https://clawhub.ai/user/nantes)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to onboard agents into a Hive swarm, manage attestations and trust scores, submit and vote on governance proposals, and back up identities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to use a remote Hive service that can automatically execute approved code changes.

Mitigation: Use it only if the hosted service and participating swarm identities are trusted, and require separate human approval before execution on sensitive hosts.

Risk: .hive backups contain private-key material.

Mitigation: Treat backups as private-key material, avoid command-line passwords, and never restore backups from untrusted sources.

Risk: Approved proposal execution may not have strong host isolation.

Mitigation: Run proposed changes only in a disposable container or VM with real isolation before allowing execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nantes/skills/the-hive-swarm-governance)
- [The Hive Repository](https://github.com/osirisConstruct/the-hive)
- [The Hive AGENTS Documentation](https://github.com/osirisConstruct/the-hive/blob/master/AGENTS.md)
- [Live Hive API](https://the-hive-o6y8.onrender.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, API calls, configuration, guidance]

**Output Format:** [Markdown guidance with bash, curl, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes CLI and API examples for onboarding, vouching, trust lookup, proposal creation, voting, and identity backup or restore.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
