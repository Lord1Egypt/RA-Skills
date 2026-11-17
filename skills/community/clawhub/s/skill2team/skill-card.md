## Description:

Design profile-based agent teams from skills, workflows, prompts, tools, or briefs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[c-narcissus](https://clawhub.ai/user/c-narcissus)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use Skill2Team to convert complex skills, workflows, prompts, tools, scripts, documentation, SOPs, or natural-language briefs into profile-based agent team designs and Codex package artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Codex package and registration helpers can persist new agents and configuration changes.

Mitigation: Inspect generated .codex/agents TOML, .codex/config.toml changes, registry manifests, and package manifests before registration or use.

Risk: Untrusted source text and local file paths can create security exposure during package generation.

Mitigation: Avoid bundle mode for untrusted source roots until path containment and symlink handling are fixed, and inspect bundled source-resources before running generated packages.

## Reference(s):

- [ClawHub Skill2Team page](https://clawhub.ai/c-narcissus/skills/skill2team)
- [Product Positioning](artifact/references/product-positioning.md)
- [Output Contracts](artifact/references/output-contracts.md)
- [Platform Adapters](artifact/references/platform-adapters.md)
- [Risk Governance](artifact/references/risk-governance.md)
- [Context Loading Policy](artifact/references/context-loading-policy.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports plus JSON, TOML, ZIP, and prompt-template files for Codex package delivery]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Design output can include architecture maps, workflow orchestration maps, conformance gates, package manifests, agent profiles, Codex TOML files, and follow-up prompt templates.]

## Skill Version(s):

1.9.2 (source: SKILL.md frontmatter metadata and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
