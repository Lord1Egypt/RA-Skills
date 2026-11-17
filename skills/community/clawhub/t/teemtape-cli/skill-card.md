## Description:

Interact with teemtape stock watchlists and anonymous notes via the teemtape CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kiwifellows](https://clawhub.ai/user/kiwifellows)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search tickers, inspect delayed stock quotes, manage teemtape watchlists, and read or post anonymous ticker notes through the teemtape CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on an external npm CLI and network access to the teemtape API.

Mitigation: Install only when teemtape access is intended, and prefer a pinned or locally reviewed version of @teemtape/cli.

Risk: Watchlist tokens and Pro access tokens grant access to teemtape watchlists.

Mitigation: Use saved configuration or environment variables instead of pasting tokens into chat, and do not echo tokens in logs or responses.

Risk: CLI note commands can create anonymous comments visible to watchlist viewers.

Mitigation: Read existing notes before posting, keep comments concise, and post only information that is safe to share.

Risk: Quote data is delayed and informational only.

Mitigation: Do not use the skill as a trading tool or present delayed quotes as real-time market data.

## Reference(s):

- [teemtape-cli Skill Page](https://clawhub.ai/kiwifellows/skills/teemtape-cli)
- [Command Reference](references/commands.md)
- [JSON Output Shapes](references/json-output.md)
- [teemtape Web App](https://www.teemtape.com)
- [teemtape API](https://api.teemtape.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands and JSON response expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Use --json for machine-readable CLI output; notes posted by the CLI can be visible to watchlist viewers.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
