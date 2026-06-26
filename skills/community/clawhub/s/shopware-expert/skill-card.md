## Description: <br>
Provides OpenClaw agents with Shopware 6 developer guidance, reference excerpts, and safety checklists for APIs, extensions, storefronts, hosting, upgrades, and integrations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[realM1lF](https://clawhub.ai/user/realM1lF) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to work on Shopware 6 APIs, plugins, apps, Administration UI, Storefront themes, headless frontends, hosting, upgrades, and commercial extensions. It helps an agent choose relevant Shopware references, check version context, and propose documented commands, code, configuration, or guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Examples or recommendations could affect production stores, customer accounts, payment setup, database state, or Admin API data. <br>
Mitigation: Use staging or copied data first, require explicit authorization for real store changes, use least-privilege credentials, and verify changes with read-after-write checks or tests. <br>
Risk: Credentials for Shopware Admin API or Store API work could be exposed in chat, logs, or committed files. <br>
Mitigation: Store secrets only in environment or skill configuration, report secret variables as set or unset without printing values, and avoid placing credentials in commands shown to users. <br>
Risk: Bundled Shopware documentation excerpts may lag current patch releases or omit edge cases. <br>
Mitigation: Confirm the target Shopware version and reconcile important API, upgrade, security, and deployment guidance with live Shopware documentation before acting. <br>
Risk: Shell or curl examples could become unsafe if untrusted user text is interpolated into commands. <br>
Mitigation: Keep gateway tool allowlists narrow, escape or allowlist command inputs, and prefer documented API patterns over ad hoc shell composition. <br>
Risk: Quick fixes to Shopware core, vendor packages, or third-party Store plugins can create brittle or unsupported changes. <br>
Mitigation: Use documented extension points, configuration, upgrades, APIs, or first-party plugin paths instead of editing core or third-party extension code directly. <br>


## Reference(s): <br>
- [Shopware Developer Documentation](https://developer.shopware.com/) <br>
- [Shopware Merchant Documentation](https://docs.shopware.com/) <br>
- [ClawHub Skill Page](https://clawhub.ai/realM1lF/shopware-expert) <br>
- [Reference Index](references/OVERVIEW.md) <br>
- [Official Sources and Versions](references/SOURCES_AND_VERSIONS.md) <br>
- [Safety and Defaults](references/SAFETY.md) <br>
- [OpenClaw Integration](references/OPENCLAW_INTEGRATION.md) <br>
- [Authentication](references/AUTH.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code, command snippets, API examples, and reference links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose curl or Shopware CLI workflows when the user's gateway policy permits them; requires SHOPWARE_BASE_URL and curl for HTTP tasks.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence, SKILL.md metadata, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
