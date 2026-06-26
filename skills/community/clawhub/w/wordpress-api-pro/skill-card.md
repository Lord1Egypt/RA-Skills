## Description: <br>
Production-grade WordPress REST API integration for managing posts, pages, media, WooCommerce products, Elementor content, SEO meta, ACF, and JetEngine fields. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[benkalsky](https://clawhub.ai/user/benkalsky) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and site operators use this skill to inspect and manage WordPress or WooCommerce content through the REST API after the user supplies credentials. It also supports public pre-sale site audits and authenticated plugin and SEO-stack discovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use WordPress or WooCommerce credentials to change live site content. <br>
Mitigation: Use a dedicated least-privilege application password, confirm the site URL and target IDs before writes, and prefer drafts unless publication is explicitly approved. <br>
Risk: Batch or multi-site operations can affect more content than intended. <br>
Mitigation: Review dry-run output first, require explicit execution flags for batch writes, and use the all-sites option only after deliberate approval. <br>
Risk: Credentials or site configuration could be exposed if stored in shared files. <br>
Mitigation: Use environment variables or local untracked config files, protect local config permissions, and rotate or revoke application passwords when no longer needed. <br>
Risk: Remote media imports and local file reads can introduce unwanted network or file access. <br>
Mitigation: Keep remote URL fetching opt-in, allow HTTPS only, restrict local file reads to approved roots, and set WP_REQUIRE_HTTPS=1 for stricter production use. <br>
Risk: Raw SEO metadata writes can create incorrect or unexpected SEO state. <br>
Mitigation: Use the Rank Math or Yoast allowlisted keys where possible and set WP_REQUIRE_ALLOWLIST=1 to block unrecognized SEO meta keys. <br>


## Reference(s): <br>
- [WordPress API Pro Skill Page](https://clawhub.ai/benkalsky/wordpress-api-pro) <br>
- [WordPress REST API Reference](references/api-reference.md) <br>
- [Gutenberg Block Format](references/gutenberg-blocks.md) <br>
- [Official WordPress REST API Documentation](https://developer.wordpress.org/rest-api/) <br>
- [PageSpeed Insights API Endpoint](https://www.googleapis.com/pagespeedonline) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON results from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include WordPress REST API results, audit summaries, configuration examples, and dry-run plans before live writes.] <br>

## Skill Version(s): <br>
3.8.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
