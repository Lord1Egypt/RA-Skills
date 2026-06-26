## Description: <br>
Automatically publish Markdown articles to a WordPress blog through the WordPress REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rainco2008](https://clawhub.ai/user/rainco2008) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and WordPress site operators use this skill to configure REST API access and publish Markdown articles, batches, drafts, categories, tags, and featured images to WordPress sites they own or administer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled diagnostic and test scripts handle WordPress credentials and JWTs unsafely, including hardcoded openow.ai credentials noted by the security review. <br>
Mitigation: Remove the bundled test, JWT, and debug scripts before installation, rotate any exposed credentials, and store WordPress passwords or tokens only in environment variables or a secret manager. <br>
Risk: The skill can modify WordPress content and includes behavior that can permanently delete content when force deletion is used. <br>
Mitigation: Use the skill only on WordPress sites you own or administer, review commands before execution, avoid scripts or options that use force=true deletion, and test publishing flows in draft or staging first. <br>
Risk: Publishing workflows may make generated or converted content public on a live WordPress site. <br>
Mitigation: Default to draft status for review, verify the target site and user permissions, and check categories, tags, excerpts, and featured images before publishing. <br>
Risk: Disabling TLS verification or accepting untrusted endpoints could expose credentials during WordPress API calls. <br>
Mitigation: Keep TLS verification enabled and connect only to trusted WordPress endpoints controlled by the site owner or administrator. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rainco2008/test-wp) <br>
- [README](artifact/README.md) <br>
- [Setup guide](artifact/setup-guide.md) <br>
- [JWT quick install guide](artifact/jwt-quick-install-guide.md) <br>
- [JWT setup checklist](artifact/jwt-setup-checklist.md) <br>
- [JWT Authentication for WP REST API plugin](https://wordpress.org/plugins/jwt-authentication-for-wp-rest-api/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, API Calls, Guidance] <br>
**Output Format:** [Markdown guidance with JavaScript, shell commands, and WordPress REST API request patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WordPress REST API access and sensitive credentials such as application passwords or JWTs.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata, package.json, skill-manifest.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
