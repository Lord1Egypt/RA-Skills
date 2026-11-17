## Description:

Provides agent guidance and scripts for web research, page fetching, authenticated browser automation, dynamic-page inspection, and network interactions through search, static fetch, curl, Jina, and Chrome CDP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aysun168](https://clawhub.ai/user/aysun168)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to route online tasks through appropriate search, static fetch, and browser automation paths, including logged-in or dynamic pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes broad browser automation over a user's logged-in Chrome session and local files.

Mitigation: Install only when that level of browser control is acceptable, use a dedicated Chrome profile with limited logins, and shut down the proxy after use.

Risk: Browser actions can affect accounts or local files through uploads, posts, purchases, forms, or similar state-changing workflows.

Mitigation: Require explicit user review before uploads, posts, purchases, form submissions, or any account-changing action.

Risk: Private or token-bearing URLs may be exposed when third-party preprocessing is used.

Mitigation: Avoid third-party preprocessing for private pages, authenticated content, and URLs containing tokens or other sensitive parameters.

## Reference(s):

- [CDP Proxy API Reference](references/cdp-api.md)
- [ClawHub Skill Page](https://clawhub.ai/aysun168/skills/web-access-bak)
- [Web Access Article](https://mp.weixin.qq.com/s/rps5YVB6TchT9npAaIWKCw)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and curl command examples, JavaScript snippets, and API call patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke local shell commands and a localhost CDP HTTP API when configured.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact metadata reports 2.4.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
