## Description:

Fetches public web pages through Jina Reader or a direct fallback and returns cleaner Markdown or JSON while applying URL validation, SSL verification, and sensitive-data checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bg1avd](https://clawhub.ai/user/bg1avd)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to retrieve clearly public webpage content as cleaned Markdown while reducing token-heavy page noise. It is not intended for internal, authenticated, signed, or secret-bearing links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive URLs or internal network content could be exposed in edge cases.

Mitigation: Use only clearly public webpages and avoid reset links, signed download URLs, internal hostnames, intranet pages, authenticated document links, and URLs containing tokens or keys.

Risk: SSRF and sensitive-data protections are incomplete for redirect validation, IPv6 handling, and Jina disclosure controls.

Mitigation: Treat the built-in checks as defense-in-depth rather than complete controls until those areas are fixed and independently reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bg1avd/skills/safe-web-fetch-for-save-token)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Markdown or JSON emitted by a Python command-line tool]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3; configurable domain allowlist, blocklist, timeout, content-size limit, user agent, and redirect limit.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
