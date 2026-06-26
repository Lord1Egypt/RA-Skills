## Description: <br>
Stock Watcher manages a personal stock watchlist and summarizes recent Chinese A-share performance using data from 10jqka.com.cn. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Robin797860](https://clawhub.ai/user/Robin797860) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to maintain a local watchlist of Chinese A-share stocks, list or clear that watchlist, and request concise recent performance summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores a local watchlist under ~/.clawdbot/stock_watcher/watchlist.txt. <br>
Mitigation: Confirm local watchlist storage is acceptable before installation and remove the file or use the cleanup commands when it is no longer needed. <br>
Risk: Stock lookups send watched stock codes to 10jqka.com.cn. <br>
Mitigation: Use the performance summary only when sharing those stock codes with the market-data site is acceptable. <br>
Risk: Clear and uninstall commands can delete the saved watchlist. <br>
Mitigation: Back up the watchlist before clearing it or uninstalling the skill if the data should be retained. <br>


## Reference(s): <br>
- [Stock Watcher release page](https://clawhub.ai/Robin797860/stock-watcher) <br>
- [10jqka stock pages](https://stockpage.10jqka.com.cn/{stock_code}/) <br>
- [Robin797860 publisher profile](https://clawhub.ai/user/Robin797860) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text command output and concise agent guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores watchlist entries locally as stock_code|stock_name lines and may include stock detail URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
