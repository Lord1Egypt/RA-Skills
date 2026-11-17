## Description:

Stock Tools manages a persistent A-share watchlist and retrieves lightweight public quotes for individual or watchlist stocks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daguniang](https://clawhub.ai/user/daguniang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to maintain a local A-share watchlist, fetch current public quote data, and summarize individual or watchlist stock performance in natural language.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled local script can overwrite arbitrary writable files through an unrestricted file-path option.

Mitigation: Keep the skill limited to its dedicated stocks-data/stocklist.txt file and avoid exposing or using the --file option.

Risk: Clear or reset requests can remove the persisted watchlist.

Mitigation: Confirm user intent before clearing or resetting saved watchlist data.

Risk: Latest quote lookups depend on a public network call and may be unavailable or lack reliable timing.

Mitigation: State when the lightweight quote source is unavailable or when quote time cannot be confirmed, and do not fabricate market data.

## Reference(s):

- [ClawHub Stock Tools skill page](https://clawhub.ai/daguniang/skills/stock-tools)
- [Sina public quote endpoint](https://hq.sinajs.cn/list=...)
- [10jqka stock detail page pattern](https://stockpage.10jqka.com.cn/{code}/)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Concise Markdown or plain text for user-facing answers; JSON is available from the quote script for structured processing.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The local watchlist script reads and writes a stock list file; quote results depend on a public market data endpoint.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
