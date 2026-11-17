## Description:

Provides OpenClaw agents with Shopware 6 guidance, checklists, and bundled documentation excerpts for APIs, extensions, storefronts, hosting, upgrades, and operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[realm1lf](https://clawhub.ai/user/realm1lf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to guide Shopware 6 work, including Admin API and Store API tasks, plugins, apps, Administration UI, storefront themes, headless frontends, hosting, upgrades, and extension decisions. It is intended to support agent planning, code guidance, configuration guidance, and cautious command/API proposals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer snippets, sudo commands, or curl-piped shell examples can make local changes that are hard to audit.

Mitigation: Keep tool allowlists narrow and independently verify sources before allowing sudo or curl-piped shell commands.

Risk: API or administrative write actions can affect Shopware data, payment, shipping, tax, checkout, or storefront behavior.

Mitigation: Use staging for risky changes, require explicit approval for destructive actions, and verify write results with read-after-write checks.

Risk: Shopware credentials or OAuth secrets could be exposed if pasted into chat or committed to files.

Mitigation: Store secrets in environment-backed configuration and show only set, unset, or masked values in agent responses.

Risk: Bundled Shopware documentation excerpts may lag the target installation or omit patch-level changes.

Mitigation: Confirm the target Shopware version and reconcile important guidance with live official documentation before breaking, security-sensitive, API-shape-critical, or deployment work.

## Reference(s):

- [ClawHub listing](https://clawhub.ai/realm1lf/skills/shopware-expert)
- [Shopware Developer Documentation](https://developer.shopware.com/)
- [Shopware User Documentation](https://docs.shopware.com/)
- [Shopware Platform Repository](https://github.com/shopware/platform)
- [Reference Index](references/OVERVIEW.md)
- [Sources and Versions](references/SOURCES_AND_VERSIONS.md)
- [OpenClaw Integration](references/OPENCLAW_INTEGRATION.md)
- [Authentication Guidance](references/AUTH.md)
- [Safety Guidance](references/SAFETY.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with code blocks, shell snippets, configuration notes, and API guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require SHOPWARE_BASE_URL and curl for HTTP-oriented Shopware tasks; guidance should be reconciled with the target Shopware version and live official documentation.]

## Skill Version(s):

1.0.5 (source: server release metadata, SKILL.md metadata, README.md bundle version, CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
