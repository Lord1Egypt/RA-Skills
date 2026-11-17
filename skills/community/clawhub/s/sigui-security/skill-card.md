## Description:

Openclaw Skill evaluates EVM, Starknet, and Aptos blockchain transactions with the Sigui Protocol and returns ALLOW, BLOCK, or ESCALATE verdicts before execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ibonon](https://clawhub.ai/user/ibonon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security reviewers, and autonomous-agent operators use this skill to check specific blockchain transactions before submitting them. It helps decide whether to proceed, block, or escalate based on a configured Sigui API endpoint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically installs Python dependencies while serving as a high-trust blockchain security gate.

Mitigation: Install it in an isolated virtual environment or container, review the dependency set, and pin Sigui SDK and rich versions before operational use.

Risk: Transaction decisions depend on the configured Sigui API endpoint and oracle response quality.

Mitigation: Configure SIGUI_API_URL only for a trusted endpoint and do not authorize real funds from unverified oracle responses.

Risk: Demo mode produces local heuristic results that are not authoritative.

Mitigation: Use demo mode only for testing and never use demo results to approve real transactions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ibonon/skills/sigui-security)
- [Sigui Homepage](https://github.com/ibonon/Sigui)
- [Sigui SDK on PyPI](https://pypi.org/project/sigui-sdk/)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with CLI commands and optional JSON evaluation output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires transaction amount, destination, action, chain, and a trusted Sigui API endpoint; ALLOW verdicts require explicit user confirmation.]

## Skill Version(s):

2.0.1 (source: frontmatter and pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
