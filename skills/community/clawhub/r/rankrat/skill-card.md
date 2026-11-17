## Description:

Rankrat lets agents analyze and manage search visibility, analytics, site audits, tags, redirects, and monitoring for sites the user controls through a self-hosted MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site operators use Rankrat to inspect search and analytics data, diagnose site issues, and manage configured provider resources for sites they control. Writable actions can submit changes such as tags, redirects, ownership proofs, and indexing requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags unpinned Docker images and an installer that can run with root privileges, creating supply-chain and installation risks.

Mitigation: Pin Docker images to reviewed digests and independently verify the installer and its integrity before running it. Avoid system-wide sudo installation unless you have reviewed and trust the installer.

Risk: The scanner review is partial: referenced local paths were missing and the downloaded installer was unavailable for review.

Mitigation: Treat the clean AIG result as inconclusive; review the installer and resolve the missing-path scan gaps before installing.

## Reference(s):

- [Setup and operator reference](references/setup.md)
- [Rankrat documentation](https://psyb0t.github.io/rankrat/)
- [Provider guides](https://psyb0t.github.io/rankrat/providers/)
- [Getting started](https://psyb0t.github.io/rankrat/getting-started/)

## Skill Output:

**Output Type(s):** [Analysis, Text, Configuration]

**Output Format:** [Structured provider data and concise text reports; configuration and provider updates when write tools are enabled]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Operations are scoped to configured provider accounts and sites; write capabilities depend on server configuration.]

## Skill Version(s):

0.21.2 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
