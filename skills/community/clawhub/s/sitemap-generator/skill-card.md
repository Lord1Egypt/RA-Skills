## Description:

Generate XML sitemaps by crawling a website for SEO, site structure audits, page discovery, or search engine submission with configurable depth, page limits, and polite delays.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnnywang2001](https://clawhub.ai/user/johnnywang2001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site owners, and SEO practitioners use this skill to crawl a trusted website and produce a standards-compliant sitemap.xml for audit or search engine submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The crawler can be directed or redirected to private or internal network targets without built-in safeguards.

Mitigation: Run only against sites you own or trust, and block private, loopback, link-local, reserved, and cloud metadata addresses while validating or disabling redirects.

Risk: Unbounded or aggressive crawling can create unwanted load on a target site.

Mitigation: Use conservative max-pages, max-depth, delay, and timeout settings that match the target site's capacity and policies.

## Reference(s):

- [Sitemaps.org Protocol 0.9](http://www.sitemaps.org/schemas/sitemap/0.9)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files]

**Output Format:** [XML sitemap file or XML on stdout with concise command-line status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports configurable crawl depth, maximum pages, delay, timeout, changefreq, priority, and output path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
