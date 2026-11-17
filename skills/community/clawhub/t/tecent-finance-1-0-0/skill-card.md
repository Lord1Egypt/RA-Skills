## Description:

Get stock prices, quotes, and compare stocks using Tencent Finance API. No API key required. Supports US stocks, China A-Shares, Hong Kong stocks. Optimized for use in mainland China.

This skill is ready for commercial/non-commercial use.

## Publisher:

[squally2k](https://clawhub.ai/user/squally2k)

### License/Terms of Use:

MIT

## Use Case:

Developers, analysts, and agent users use this skill to fetch quick stock prices, detailed quotes, stock comparisons, and symbol search results from Tencent Finance for US stocks, China A-shares, Hong Kong stocks, and popular cryptocurrencies.

### Deployment Geography for Use:

Global, with documentation noting optimization for mainland China network environments.

## Known Risks and Mitigations:

Risk: The install notes reference a tfin executable that is not present in the provided artifact evidence.

Mitigation: Verify the tfin implementation from a trusted source before installing or executing the skill.

Risk: Installing dependencies globally or creating a /usr/local/bin symlink can affect the host environment.

Mitigation: Install reviewed, pinned dependencies in a dedicated virtual environment and avoid administrator privileges unless necessary.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/squally2k/skills/tecent-finance-1-0-0)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and command output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Finance data coverage excludes India NSE/BSE, options, and dividends according to the artifact documentation.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
