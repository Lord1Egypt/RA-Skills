## Description:

Build next-session A-share game plans from market structure, overnight macro shocks, policy timing, and watchlist leadership.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huangrichao2020](https://clawhub.ai/user/huangrichao2020)

### License/Terms of Use:

MIT-0

## Use Case:

External analysts and developers use this skill to turn A-share market structure, overnight macro events, policy timing, and watchlists into a next-session desk plan with scenarios and opening-window checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: One-line clone-and-run installation can execute local code before independent review.

Mitigation: Review, pin, or verify the installer and scripts before running bundled install commands.

Risk: The optional news iterator can run as a recurring background process with network polling and local state under ~/.uwillberich.

Mitigation: Install the background service only when recurring polling is desired, and confirm the stop, unload, and removal process before enabling it.

Risk: Runtime environment files may contain credentials.

Mitigation: Store only the Eastmoney key needed by this skill in the runtime env file and avoid adding unrelated secrets to skill-local .env files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huangrichao2020/skills/uwillberich)
- [Project homepage](https://github.com/huangrichao2020/uwillberich)
- [Methodology](references/methodology.md)
- [Data Sources](references/data-sources.md)
- [Opening Window Template](references/opening-window-template.md)
- [Message Iterator](references/message-iterator.md)
- [Cross-Cycle Watchlist](references/cross-cycle-watchlist.md)
- [Event Regime Watchlists](references/event-regime-watchlists.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with optional JSON, JSONL, SQLite, and shell-command artifacts from bundled scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 and an Eastmoney API key for MX-backed workflows; some optional workflows perform recurring network polling and write local state.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
