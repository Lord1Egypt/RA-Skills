## Description:

Daily Stock Analysis v2.1 is an LLM-driven stock analysis skill for A-share, Hong Kong, and U.S. equities, with technical and fundamental analysis, market and sector reviews, agent Q&A, and multi-channel report delivery.

This skill is for research and development only.

## Publisher:

[same1317](https://clawhub.ai/user/same1317)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to generate daily stock analysis, market reviews, sector summaries, and stock-strategy Q&A for A-share, Hong Kong, and U.S. market workflows. The artifact states it is for learning and research and does not provide investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup and update helpers can install or refresh mutable upstream code that was not part of the reviewed local package.

Mitigation: Use the reviewed local package where possible; avoid setup or update helpers unless the upstream repository is pinned to a reviewed commit, and do not run them as root.

Risk: Configuration can contain API keys, webhook URLs, chat identifiers, and email credentials used for outbound reports.

Mitigation: Use least-privilege credentials, keep push delivery disabled until explicitly configured, and remove any backup environment files that contain secrets.

Risk: AI analysis and pushed reports may disclose prompts, holdings, watchlists, or generated financial analysis to third-party services.

Mitigation: Review configured AI providers and push channels before use, and treat generated reports as data shared outside the local workspace.

Risk: Generated stock analysis may be incorrect, stale, or unsuitable for investment decisions.

Mitigation: Use the output for learning and research only, verify market data independently, and do not treat generated analysis as financial advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/same1317/skills/stock-daily-analysis-v2)
- [akshare data source](https://github.com/akfamily/akshare)
- [OpenClaw market-data skill](https://github.com/chjm-ai/openclaw-market-data)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON-like Python dictionaries, and command-line output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May send generated reports through configured webhook or email channels when push delivery is enabled.]

## Skill Version(s):

2.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
