## Description:

WordPress API Pro helps agents manage WordPress and WooCommerce content through REST APIs, including posts, pages, media, Elementor content, SEO metadata, ACF, JetEngine fields, and site audits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[benkalsky](https://clawhub.ai/user/benkalsky)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site operators, and content teams use this skill to inspect, draft, create, update, and audit WordPress or WooCommerce sites after supplying explicit credentials and approval for live writes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured WordPress or WooCommerce credentials can permit live content changes.

Mitigation: Use dedicated least-privileged credentials, confirm target site, IDs, fields, status, and final action before writes, prefer drafts, and review dry-run output before batch or seed execution.

Risk: Local configuration files may contain production credentials.

Mitigation: Keep config/sites.json local and locked down, prefer environment variables or a secret manager, and avoid committing production credentials.

Risk: PageSpeed audits may disclose private or confidential URLs to Google.

Mitigation: Run PageSpeed audits only for public URLs or omit PageSpeed checks for confidential sites.

Risk: Remote media fetches and local file reads can expose unintended resources if allowed too broadly.

Mitigation: Keep remote media URLs opt-in, use HTTPS public URLs, and scope local file reads with WP_ALLOWED_FILE_ROOTS.

Risk: Dependency installation can introduce environment or patch-management risk.

Mitigation: Install dependencies in a virtual environment and keep the requests dependency within the documented secure version range.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/benkalsky/skills/wordpress-api-pro)
- [WordPress REST API Reference](references/api-reference.md)
- [Gutenberg Block Format](references/gutenberg-blocks.md)
- [Official WordPress REST API Documentation](https://developer.wordpress.org/rest-api/)
- [Google PageSpeed Online API Endpoint](https://www.googleapis.com/pagespeedonline)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, shell command examples, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or run WordPress REST API operations, audits, and dry-run plans depending on user approval and configured credentials.]

## Skill Version(s):

3.9.5 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
