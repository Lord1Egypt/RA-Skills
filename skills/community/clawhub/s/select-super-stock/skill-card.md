## Description: <br>
Select Super Stock helps analyze and screen stocks for medium- to long-term investment research using trend, technical, fundamental, dividend, industry-cycle, and blacklist criteria. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[georgetao730](https://clawhub.ai/user/georgetao730) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to request single-stock analysis or screen candidate equities for longer-term investment research. Its reports should be treated as research support, not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Financial analysis may be inaccurate, stale, or misleading; the security evidence says the skill overstates market coverage and screening rigor. <br>
Mitigation: Treat outputs as research support only, verify Hong Kong and U.S. coverage, screening results, financial metrics, news claims, and cached data freshness independently, and do not rely on the skill as investment advice. <br>
Risk: The skill runs local Python and fetches market data, so results can be affected by dependency availability, network failures, API limits, or stale cache behavior. <br>
Mitigation: Review the scripts and dependencies before execution, confirm network and data-source assumptions, and check cache timestamps before using any generated report. <br>


## Reference(s): <br>
- [Select Super Stock ClawHub page](https://clawhub.ai/georgetao730/select-super-stock) <br>
- [Model A long-term uptrend examples](artifact/references/model-a-examples.md) <br>
- [Model B historical-low rebound examples](artifact/references/model-b-examples.md) <br>
- [Blacklist stock patterns](artifact/references/blacklist-patterns.md) <br>
- [Industry cycle guide](artifact/references/industry-cycles.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown report or JSON summary, with optional Python command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May fetch AKShare market data and use cached data with a 24-hour freshness window when supporting cache utilities are available.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata and artifact/_meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
