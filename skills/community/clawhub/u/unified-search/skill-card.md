## Description: <br>
统一搜索技能！中文用百度，英文用 DuckDuckGo，加密货币用 CoinGecko <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coder-knock](https://clawhub.ai/user/coder-knock) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to run web searches that route Chinese queries to Baidu, English queries to DuckDuckGo, and cryptocurrency price queries to CoinGecko. It returns source-labeled results that can be used for quick research or command-line lookup workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports that the skill can execute an unbundled neighboring DuckDuckGo helper. <br>
Mitigation: Inspect or install only a trusted ddg-search helper before using English-search routing. <br>
Risk: Search terms are sent to external search and price-data providers. <br>
Mitigation: Do not submit secrets, private identifiers, regulated data, or other sensitive content as search queries. <br>
Risk: The artifact includes a shell-exec example pattern that can be unsafe with untrusted input. <br>
Mitigation: Pass user input as arguments to trusted scripts and avoid copying shell execution examples with unsanitized values. <br>
Risk: The security summary notes inconsistent install and run scope. <br>
Mitigation: Confirm the intended install folder and script paths before deployment. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/coder-knock/unified-search) <br>
- [Publisher profile](https://clawhub.ai/user/coder-knock) <br>
- [Baidu Search](https://www.baidu.com) <br>
- [Bing Search](https://www.bing.com) <br>
- [CoinGecko](https://www.coingecko.com) <br>
- [CoinGecko simple price API endpoint](https://api.coingecko.com/api/v3/simple/price) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [JSON arrays or formatted terminal text with titles, URLs, snippets, and source labels] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search queries are sent to external providers; formatted output truncates snippets for readability.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
