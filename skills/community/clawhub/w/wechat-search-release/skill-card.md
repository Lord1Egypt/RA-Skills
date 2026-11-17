## Description:

Search WeChat Official Account articles using OpenClaw's web search and fetch capabilities with compliance-focused design.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jixsonwang](https://clawhub.ai/user/jixsonwang)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to search public WeChat Official Account articles, apply recency or date filters, and return article metadata in text, JSON, or markdown formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: External web searches may expose search terms and return untrusted URLs.

Mitigation: Avoid sensitive search terms and review returned links before opening or sharing them.

Risk: The security scan reports that compliance claims are weaker than advertised.

Mitigation: Use a fixed version that enforces or removes the claimed robots.txt, rate-limit, and User-Agent behavior.

Risk: Search results may include deceptive links that are treated as valid WeChat results.

Mitigation: Validate result hostnames exactly and treat non-matching URLs as untrusted.

Risk: Query construction and dependencies may need hardening.

Mitigation: URL-encode queries and pin dependencies before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jixsonwang/skills/wechat-search-release)
- [Weixin Sogou search endpoint](https://weixin.sogou.com/weixin?type=2&query={query})

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Text, JSON, or Markdown search results with article metadata and URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns up to five recent articles by default, with configurable result limits, date filters, strategy selection, cache duration, request delay, and user agent.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
