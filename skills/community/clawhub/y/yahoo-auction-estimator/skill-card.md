## Description:

日本雅虎拍卖商品估价工具 - 自动获取商品信息、查询历史成交价、计算建议出价

This skill is ready for commercial/non-commercial use.

## Publisher:

[hiddenpuppy](https://clawhub.ai/user/hiddenpuppy)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to estimate Yahoo Japan auction items by fetching current listing details, comparing historical aucfree sale prices, and calculating a suggested bid.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Auction IDs or proxy settings may lead to unintended shell command execution.

Mitigation: Use only trusted auction IDs and prefer a patched version that validates inputs and uses safe argument arrays or a native HTTP client.

Risk: Proxy credentials may be printed in CLI output.

Mitigation: Avoid embedding credentials in PROXY_SOCKS5 and run the skill only in environments where console output is appropriately protected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hiddenpuppy/skills/yahoo-auction-estimator)
- [Yahoo! Auctions item pages](https://auctions.yahoo.co.jp/)
- [aucfree historical auction search](https://aucfree.com/)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text CLI report with item title, keyword, current price, end time, historical price range, suggested bid, and status.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node, curl, and PROXY_SOCKS5 for proxy access.]

## Skill Version(s):

1.0.3 (source: server release evidence; artifact package metadata lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
