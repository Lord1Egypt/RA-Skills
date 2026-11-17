## Description:

Guides setup of the Wyckoff CLI and optional MCP server, then produces auditable A-share Wyckoff volume-price analysis, data-source fallbacks, portfolio actions, and charting guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youngcan-wang](https://clawhub.ai/user/youngcan-wang)

### License/Terms of Use:

MIT-0

## Use Case:

External traders, analysts, and developers use this skill to onboard the Wyckoff command-line and MCP tooling, retrieve and audit A-share market data, and generate Wyckoff-style analysis with portfolio actions such as add, reduce, hold, exit, or switch.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow offers a curl-to-bash installer and package installation commands.

Mitigation: Prefer a pinned, verified package installed in a virtual environment, and inspect any install script before execution.

Risk: The skill asks users to handle passwords, API keys, and data-source tokens through CLI and MCP configuration flows.

Mitigation: Avoid putting secrets directly in shell commands or shared MCP config files; use secure local secret handling and review shell history exposure.

Risk: The optional MCP server can persist as a tool integration, read saved Wyckoff credentials, and expose portfolio and trading-adjacent actions.

Mitigation: Register the MCP server only in trusted clients, review tool permissions, and require human confirmation before any real portfolio-changing action.

Risk: The workflow includes a paid TickFlow referral link.

Mitigation: Treat the link as commercial steering unless the publisher clearly discloses the relationship and provides comparable data-source alternatives.

Risk: Trading guidance may be incorrect, stale, or unsuitable for the user's financial situation.

Mitigation: Use outputs as decision support only, verify market data independently, and route final investment decisions through qualified human review.

## Reference(s):

- [Wyckoff Analysis GitHub Repository](https://github.com/YoungCan-Wang/Wyckoff-Analysis)
- [Wyckoff Analysis Web Registration](https://wyckoff-analysis.pages.dev/)
- [Tushare Data Source](https://tushare.pro/)
- [TickFlow Registration](https://tickflow.org/auth/register?ref=5N4NKTCPL4)
- [Model Context Protocol](https://modelcontextprotocol.io/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with tables, inline shell commands, optional Python plotting code, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes timestamp and trading-session verdict, source audit table, Wyckoff structural analysis, portfolio actions, and plotting notes when allowed.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
