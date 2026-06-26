## Description: <br>
Screens A-share main-board stocks near market close using Tencent Finance real-time data, Baostock historical data, and Yang Yongxing strategy filters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dxyu94](https://clawhub.ai/user/dxyu94) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run an end-of-day stock-screening workflow for A-share main-board stocks. It loads a prepared stock list, applies real-time and historical-data filters, and prints matching candidates to the terminal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests for market data. <br>
Mitigation: Run it in a trusted Python environment with approved network access to the documented market-data sources. <br>
Risk: The stock universe is loaded from main_board_stocks.json. <br>
Mitigation: Verify the input file path and source before running the screen. <br>
Risk: The skill writes a local market_cap_cache.json file. <br>
Mitigation: Run it from a dedicated skill directory and review or clear the cache when stale data would affect screening. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dxyu94/yang-selection) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text output with local JSON cache file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates market_cap_cache.json and depends on main_board_stocks.json from the query-main-board-stocks workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
