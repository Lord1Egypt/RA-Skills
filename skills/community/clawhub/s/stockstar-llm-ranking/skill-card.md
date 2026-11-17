## Description:

Queries StockStar Technology Channel large-model invocation leaderboards for day and week rankings, including model, publisher, token volume, change direction, percentage change, new-entry status, and update date.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stockstar1996](https://clawhub.ai/user/stockstar1996)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve and summarize StockStar LLM invocation rankings in Chinese-language leaderboard workflows. It supports complete leaderboard views, day or week filtering, top-N summaries, and model or vendor search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes live outbound requests to tech.stockstar.com, so results depend on network availability and the remote page response.

Mitigation: Use it only for explicit StockStar leaderboard requests and handle network failures by asking the user to retry later.

Risk: The parser depends on the StockStar page's embedded leaderboard structure, so page changes can produce missing or incomplete rankings.

Mitigation: Check for empty or failed results before presenting rankings, and avoid fabricating leaderboard data when parsing fails.

Risk: The skill is mainly intended for Chinese-language ranking queries and may be less reliable for unrelated prompts.

Mitigation: Trigger it only for StockStar LLM invocation leaderboard, day/week ranking, top-N, model search, or vendor search requests.

## Reference(s):

- [StockStar Technology Channel](https://tech.stockstar.com/)
- [ClawHub skill page](https://clawhub.ai/stockstar1996/skills/stockstar-llm-ranking)
- [Publisher profile](https://clawhub.ai/user/stockstar1996)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, guidance]

**Output Format:** [Chinese-language Markdown summaries derived from JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches the fixed public StockStar page and can emit JSON with source, data_source, updated_at, periods, and matches fields.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
