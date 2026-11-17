## Description:

Free trust intelligence for AI agents that provides MCP and REST access for trust scoring, sybil detection, sock puppet scanning, fake review detection, reviewer wallet behavior profiling, agent comparison, commerce data, and network stats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rnwy](https://clawhub.ai/user/rnwy)

### License/Terms of Use:

MIT-0

## Use Case:

External agents, developers, and operators use this skill to check whether an agent or wallet appears trustworthy before transacting, hiring, accepting work, or relying on reviews. It supports read-only trust checks, reviewer analysis, wallet age checks, agent comparison, network statistics, and commerce lookups, with separate registration, messaging, vouching, and marketplace actions that should require approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autonomous write actions may create persistent public identity, reputation, messaging, marketplace, or on-chain records.

Mitigation: Permit read-only trust checks by default and require explicit approval before registration, wallet submission, batch registration, vouching, messaging, or marketplace job actions.

Risk: Trust scores, reviewer analysis, and scanner results may be used as final fraud determinations without human or policy review.

Mitigation: Treat outputs as decision support and review the score math, raw data, and business policy before making high-impact trust, payment, identity, or marketplace decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rnwy/skills/rnwy)
- [RNWY MCP Endpoint](https://rnwy.com/api/mcp)
- [RNWY API Documentation](https://rnwy.com/api)
- [RNWY Scanner](https://rnwy.com/scanner)
- [Artifact README](artifact/README.md)
- [Artifact FAQ](artifact/FAQ.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration snippets, shell commands, REST URLs, and JSON API responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include external RNWY MCP or REST responses for trust scores, reviewer analysis, wallet age, comparisons, network statistics, commerce data, and identity or marketplace workflows.]

## Skill Version(s):

1.0.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
