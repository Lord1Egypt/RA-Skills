## Description:

Check subdomains for potential takeover vulnerabilities by detecting dangling DNS records pointing to unclaimed services such as GitHub Pages, Heroku, and AWS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hostilespider](https://clawhub.ai/user/hostilespider)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security teams use this skill to check authorized subdomain lists for DNS records that may point to unclaimed third-party services. It supports passive DNS-only review and active verification that can produce network requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Active scans make DNS and HTTP requests against supplied domains.

Mitigation: Run active mode only for domains you control or are permitted to test; use --passive for untrusted lists.

Risk: The release metadata lists bash and dig but the script also uses curl for active HTTP checks.

Mitigation: Confirm curl is available before active scans or use --passive when curl is unavailable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hostilespider/skills/subdomain-takeover)
- [Publisher profile](https://clawhub.ai/user/hostilespider)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands; the checker can also emit JSON scan summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write scan findings to an output file when requested.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
