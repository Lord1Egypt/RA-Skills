## Description: <br>
日本雅虎拍卖商品估价工具 - 自动获取商品信息、查询历史成交价、计算建议出价 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HiddenPuppy](https://clawhub.ai/user/HiddenPuppy) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and purchasing agents use this skill to estimate Yahoo Japan auction items by looking up current listing information, historical aucfree sale prices, and a suggested bid. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release security summary reports that crafted item IDs or proxy settings can execute unintended local shell commands. <br>
Mitigation: Run only with trusted, normal-looking auction IDs and a proxy value that contains no credentials or shell metacharacters; review the script before installation. <br>
Risk: The skill prints proxy configuration in output, which can expose sensitive proxy details if credentials are embedded in the proxy URL. <br>
Mitigation: Use a credential-free local proxy value when possible and avoid sharing logs that include proxy settings. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/HiddenPuppy/yahoo-auction-estimator) <br>
- [Yahoo! Auctions Japan](https://auctions.yahoo.co.jp/) <br>
- [aucfree historical auction search](https://aucfree.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Console text with item summaries, historical prices, suggested bids, and status labels] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node, curl, and the PROXY_SOCKS5 environment variable for proxy access.] <br>

## Skill Version(s): <br>
1.0.3 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
