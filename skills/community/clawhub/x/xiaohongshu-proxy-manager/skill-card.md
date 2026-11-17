## Description:

Manages proxy pools, account-to-proxy mappings, latency checks, and exportable proxy settings for Xiaohongshu multi-account workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[utopiabenben](https://clawhub.ai/user/utopiabenben)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and operators use this skill to configure, test, list, and retrieve proxy settings for Xiaohongshu account workflows. The release evidence warns that it should not be used for deceptive multi-account automation or ban evasion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the skill is aimed at evading Xiaohongshu account-abuse controls.

Mitigation: Use only for legitimate proxy configuration that complies with Xiaohongshu policies; do not use it for deceptive multi-account automation or ban evasion.

Risk: Proxy credentials may be entered through command-line flags, stored in configuration, or printed in proxy URLs.

Mitigation: Avoid passing paid proxy passwords through shell history, restrict permissions on proxy configuration files, and treat printed proxy URLs as secrets.

Risk: Traffic and account activity routed through untrusted proxies can expose sensitive data or reduce account security.

Mitigation: Use trusted proxy providers, avoid free or unknown proxies for sensitive workflows, and rotate or disable unhealthy proxies after checks fail.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/utopiabenben/skills/xiaohongshu-proxy-manager)
- [Publisher profile](https://clawhub.ai/user/utopiabenben)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal text with bash, Python, curl, and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate or print proxy URLs that include credentials; treat outputs as secrets.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
