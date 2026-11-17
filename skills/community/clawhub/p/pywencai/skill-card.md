## Description:

PyWenCai helps agents query iWenCai market data with Chinese natural-language prompts for A-shares, indices, funds, Hong Kong and U.S. stocks, convertible bonds, and related markets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coderwpf](https://clawhub.ai/user/coderwpf)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure PyWenCai and ask Chinese natural-language questions against iWenCai market datasets. It is intended for data retrieval and screening workflows across stocks, indices, funds, convertible bonds, and related financial instruments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an authenticated iWenCai session cookie, which can expose account access if copied into prompts, files, logs, screenshots, or shared folders.

Mitigation: Treat WENCAI_COOKIE like a password, keep it out of shared material, store it in a local environment variable or secret store, and rotate it if exposed.

Risk: The install guidance relies on mutable third-party package resolution, including upgrade-style installation.

Mitigation: Use pinned, reviewed dependency versions or a lockfile and run the skill in a least-privilege environment with only the network and files it needs.

Risk: Queries depend on the external iWenCai service and may return empty data or fail when cookies expire, rate limits apply, or the service changes.

Mitigation: Validate returned data before use, handle None or exceptions, reduce request frequency, and refresh the cookie only through the official iWenCai login flow.

## Reference(s):

- [ClawHub pywencai skill page](https://clawhub.ai/coderwpf/skills/pywencai)
- [iWenCai](https://www.iwencai.com/)
- [PyWenCai GitHub project](https://github.com/zsrl/pywencai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include dependency installation, cookie configuration, query examples, result validation, and error handling advice.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
