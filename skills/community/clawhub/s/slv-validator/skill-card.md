## Description:

Deploys and manages Solana validators on mainnet and testnet using guided agent workflows, Ansible playbooks, and Jinja2 templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[poppin-fumi](https://clawhub.ai/user/poppin-fumi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and validator operators use this skill to collect deployment variables, generate inventory configuration, run or propose Ansible commands, and monitor Solana validator lifecycle operations across mainnet and testnet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to run high-impact Ansible automation from an unaudited mutable template directory.

Mitigation: Review the resolved ~/.slv/template playbooks before any run, use the skill only on intended validator hosts, and require explicit confirmation before identity changes, restarts, user creation, firewall/systemd changes, or ledger cleanup.

Risk: Setup guidance includes installer patterns that can pull mutable dependencies.

Mitigation: Avoid curl-to-shell installers where possible and prefer pinned, verified dependencies before installing or updating validator tooling.

## Reference(s):

- [SLV Validator Skill Page](https://clawhub.ai/poppin-fumi/skills/slv-validator)
- [ValidatorsDAO/slv](https://github.com/ValidatorsDAO/slv)
- [ERPC](https://erpc.global/en/)
- [Agave Source](https://github.com/anza-xyz/agave.git)
- [Jito Solana Source](https://github.com/jito-foundation/jito-solana.git)
- [Firedancer Source](https://github.com/firedancer-io/firedancer.git)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and YAML configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Ansible inventory variables, dry-run commands, validator health checks, and confirmation prompts before high-impact operations.]

## Skill Version(s):

0.13.15 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
