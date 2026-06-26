## Description: <br>
Enables OpenClaw agents to manage WordPress content, media, settings, plugins, themes, WooCommerce, Elementor, REST workflows, and code under wp-content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[realM1lF](https://clawhub.ai/user/realM1lF) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, site owners, and administrators use this skill to connect an OpenClaw agent to an existing WordPress site, configure credentials and tools, and perform content, site administration, plugin/theme, WooCommerce, and Elementor tasks with least-privilege safeguards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is intended to operate on WordPress sites using sensitive application-password credentials and optional write-capable tools. <br>
Mitigation: Use a dedicated least-privilege WordPress application password, keep secrets out of chat, Git, screenshots, and backups, and store credentials only in environment or OpenClaw configuration. <br>
Risk: Optional WP-CLI, media, and plugin-file tools can make broad or destructive changes when enabled. <br>
Mitigation: Start on staging, allow only the specific tools and WP-CLI prefixes needed, back up the site before destructive or broad write operations, and require explicit approval for deletes, database drops, theme switches, or wide-ranging updates. <br>
Risk: The companion plugin and optional MU helper expand the trusted code and access surface beyond the text-only skill bundle. <br>
Mitigation: Review the separate wordpress-site-tools plugin before installing it and copy optional MU helper code only from a trusted full source checkout when that helper is needed. <br>


## Reference(s): <br>
- [WordPress Expert README](artifact/README.md) <br>
- [Connect WordPress to OpenClaw](artifact/references/CONNECTING.md) <br>
- [Before install: trust, credentials, and blast radius](artifact/references/PRE_INSTALL_AND_TRUST.md) <br>
- [Safety and defaults](artifact/references/SAFETY.md) <br>
- [Tools: decision tree](artifact/references/TOOLING.md) <br>
- [WP-CLI allowlist presets](artifact/references/WPCLI_PRESETS.md) <br>
- [OpenClaw integration policy](artifact/references/OPENCLAW_INTEGRATION.md) <br>
- [OpenClaw WordPress companion plugin](https://github.com/realM1lF/openclaw-wordpress-tool) <br>
- [ClawHub listing](https://clawhub.ai/realM1lF/wordpress-expert) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with command snippets, JSON/JSON5 configuration examples, REST/WP-CLI instructions, and code-oriented WordPress development guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May depend on configured WordPress REST credentials, optional WP-CLI access, and optional companion plugin tools.] <br>

## Skill Version(s): <br>
1.0.12 (source: ClawHub release metadata; artifact metadata.version reports 1.1.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
