## Description:

Cross-platform second-hand price comparison and in-depth item evaluation for marketplace listings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fastislow](https://clawhub.ai/user/fastislow)

### License/Terms of Use:

MIT

## Use Case:

External users and shopping assistants use this skill to compare second-hand marketplace listings, shortlist deals, and evaluate seller trust, condition, value, and purchase risk.

### Deployment Geography for Use:

United Kingdom

## Known Risks and Mitigations:

Risk: Browser access, network access, URL handling, and image fetching are broad enough to require review before normal use.

Mitigation: Install only after reviewing the browser and network implications, use a dedicated Chrome profile for bb-browser, and avoid untrusted listing URLs.

Risk: The skill depends on bb-browser adapters to access marketplace pages.

Mitigation: Pin and verify bb-browser before installing it, then run the documented adapter install and smoke-test flow before relying on results.

Risk: Optional vision analysis can send listing images to a configured OpenAI-compatible API endpoint.

Mitigation: Enable vision analysis only with a trusted HTTPS endpoint and a provider-specific API key.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fastislow/skills/used-price-compare)
- [ClawHub Project Homepage](https://clawhub.ai/fastislow/used-price-compare)
- [Chinese Reference](references/zh-CN.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with tables and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results should include marketplace platform, price, clickable listing links, seller trust, condition, score, and buy recommendation when available.]

## Skill Version(s):

0.6.4 (source: frontmatter, pyproject.toml, CHANGELOG, released 2026-05-21)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
