## Description: <br>
Smart Money Miner helps agents discover and filter high-performing Solana and BNB Chain wallet addresses by analyzing public token-trading data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jackydai-bc](https://clawhub.ai/user/Jackydai-bc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent users use this skill to collect token trader data, filter wallets by profitability and win-rate metrics, and produce a JSON shortlist for further review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill produces wallet lists from public crypto trading data that could be mistaken for financial advice. <br>
Mitigation: Review generated wallet lists and supporting metrics before taking any financial action. <br>
Risk: The skill makes external API requests and writes a local results file. <br>
Mitigation: Install only in environments where outbound API access and local JSON output are acceptable. <br>
Risk: Broad trigger language could activate the skill for adjacent non-crypto requests. <br>
Mitigation: Maintain narrower activation language when customizing the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Jackydai-bc/smart-money-miner) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and generated JSON result files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes smart_money_results.json and may use an optional skip-addresses JSON file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter states 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
