## Description:

Website crawling, auditing, offline cloning, and markdown export using SiteOne Crawler (Rust).

This skill is ready for commercial/non-commercial use.

## Publisher:

[tsingliuwin](https://clawhub.ai/user/tsingliuwin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site operators use this skill to run SiteOne Crawler for website audits, offline clones, markdown exports, sitemap generation, CI quality gates, and controlled load tests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically install and run an unverified third-party crawler binary.

Mitigation: Review before installation, trust the upstream release source, or pin and verify the binary before allowing execution.

Risk: HTML reports and crawl results may be uploaded externally when upload options are enabled.

Mitigation: Keep reports local by default and enable upload only when the destination and retention settings are intentional and trusted.

Risk: Crawling, stress testing, robots bypass, certificate bypass, cookies, headers, and authentication options can affect third-party systems or expose sensitive data.

Mitigation: Use these options only on sites you are authorized to test, prefer conservative worker and rate limits, and avoid passing secrets on shared systems.

## Reference(s):

- [SiteOne Crawler CLI Parameters Reference](references/cli-params.md)
- [ClawHub Skill Page](https://clawhub.ai/tsingliuwin/skills/siteone-crawler)
- [SiteOne Crawler Latest Release API](https://api.github.com/repos/janreges/siteone-crawler/releases/latest)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and file outputs such as HTML reports, JSON results, text output, markdown exports, sitemaps, and offline site files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Crawler runs may write local files, optionally upload reports when requested, and return non-zero exit codes for CI threshold failures.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
