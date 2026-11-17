## Description:

Queries StockStar investor-relations Q&A and signal-mining data for A-share listed companies, including structured signals, importance ratings, marginal changes, tags, sentiment, and reply quality.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stockstar1996](https://clawhub.ai/user/stockstar1996)

### License/Terms of Use:

MIT-0

## Use Case:

External investors, analysts, and finance-focused agents use this skill to look up public investor-interaction Q&A and structured signal-mining results for one A-share listed company at a time. It helps search stocks, inspect tags, filter Q&A by domain or tag, and summarize returned StockStar data without fabricating unsupported facts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad finance phrasing may trigger public StockStar lookups when the user intended another finance task.

Mitigation: Use explicit prompts for investor Q&A, tags, signal data, or StockStar lookups, and ask for clarification when the requested finance task is ambiguous.

Risk: Returned investor Q&A and signal data may be unavailable, empty, delayed, or narrower than the user's requested market scope.

Mitigation: State when data is empty or limited, preserve the A-share-only scope, and avoid presenting missing or inferred details as source-backed facts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/stockstar1996/skills/stockstar-investor)
- [ClawHub Publisher Profile](https://clawhub.ai/user/stockstar1996)
- [StockStar Investor Interaction](https://stock.stockstar.com/dmhd)
- [StockStar Signal Page Template](https://stock.stockstar.com/dmhd/signal/{stockid})
- [StockStar Search Suggest Endpoint](https://q.ssajax.cn/info/handler/xsuggesthandler.ashx)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, guidance]

**Output Format:** [Markdown summaries with CLI command guidance and parsed JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One stock per query; A-share coverage only; source data must come from StockStar responses.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
