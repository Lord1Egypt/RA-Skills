## Description:

AI Agent Skill for GitHub project analysis and nad.fun token launch. Analyzes repos, generates token identity/promo, and launches on nad.fun.

This skill is ready for commercial/non-commercial use.

## Publisher:

[starrftw](https://clawhub.ai/user/starrftw)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use Tokenbroker to analyze GitHub projects, propose token identity and launch metadata, prepare nad.fun upload assets, and draft promotional launch content. The skill supports launch preparation and orchestration, with sensitive wallet and deployment steps requiring explicit review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential handling during setup can expose GitHub tokens, API keys, or wallet private keys if copied into shell commands or plaintext files without care.

Mitigation: Use a pinned, verified installer; avoid exporting real GitHub tokens into install commands; prefer host-injected credentials; and review any .env file and permissions before use.

Risk: nad.fun uploads, mainnet preparation, or delegated token deployment can create externally visible assets or lead to on-chain actions.

Mitigation: Prefer testnet-only configuration and require explicit human confirmation before uploads, mainnet preparation, transaction signing, or downstream deployment.

Risk: Generated token identity, investment thesis, reputation, or promotional text may overstate project quality or launch legitimacy.

Mitigation: Review generated metadata, claims, social drafts, and builder reputation outputs before publishing or using them for launch decisions.

## Reference(s):

- [Tokenbroker ClawHub page](https://clawhub.ai/starrftw/skills/tokenbroker)
- [nad.fun agent documentation](https://nad.fun/llms.txt)
- [nad.fun skill documentation](https://nad.fun/skill.md)
- [monad-development skill reference](https://gist.github.com/moltilad/31707d0fc206b960f4cbb13ea11954c2)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, TypeScript examples, JSON-style launch metadata, shell commands, and generated social post drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include token identity proposals, launch preparation data, nad.fun API upload results, salt mining results, and promotional copy for X, Telegram, Discord, and Reddit.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact SKILL.md frontmatter reports 1.01 and artifact/_meta.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
