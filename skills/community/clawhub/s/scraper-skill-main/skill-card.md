## Description:

Search Harvester discovers candidate websites for link building and outreach by routing low-volume search queries through rotating Tor exits, harvesting results from DuckDuckGo HTML and Marginalia, deduplicating them, and exporting a scored candidate list.

This skill is ready for commercial/non-commercial use.

## Publisher:

[toniilic](https://clawhub.ai/user/toniilic)

### License/Terms of Use:

MIT-0

## Use Case:

SEO practitioners, link builders, founders, marketers, and developers use this skill to discover directories, submission platforms, blogs, and listicles for site outreach when direct datacenter-IP search is blocked by captchas or anti-bot controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tor-based search scraping may be disallowed by an organization's policy, site terms, or local rules.

Mitigation: Install and run the skill only after confirming Tor-based scraping is approved for the environment and target sites.

Risk: Public HTTP proxies can expose sensitive queries or behave unreliably.

Mitigation: Avoid public proxy fallback for sensitive queries and require explicit user approval before enabling any proxy fallback.

Risk: Running Tor with broad privileges or uncontrolled output paths can increase operational exposure.

Mitigation: Run Tor under a dedicated unprivileged service account with controlled configuration and output paths.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/toniilic/skills/scraper-skill-main)
- [Publisher profile](https://clawhub.ai/user/toniilic)
- [Project homepage](https://github.com/toniilic/scraper-skill)
- [OpenClaw skill format documentation](https://docs.openclaw.ai/clawhub/skill-format)
- [OpenClaw publishing documentation](https://docs.openclaw.ai/clawhub/publishing)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Ranked markdown candidate list with URLs, liveness status, barrier type, and suggested action; may also include shell commands and JSON-style reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Linux with tor, curl, python3, and nc; expects a local Tor SOCKS and control-port setup before harvesting.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
