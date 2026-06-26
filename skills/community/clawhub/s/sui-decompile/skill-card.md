## Description: <br>
Fetch on-chain Sui Move contract source code and let your agent explain how smart contracts work. Scrape from Suivision/Suiscan explorers, analyze DeFi protocols, and understand any contract on Sui. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EasonC13](https://clawhub.ai/user/EasonC13) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and smart contract analysts use this skill to fetch and study Sui Move package source or decompiled code from public Sui explorers, including multi-module packages and DeFi protocol examples. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may guide browser-based scraping of public Sui explorer pages. <br>
Mitigation: Confirm that scraping complies with the target explorer's terms and limit use to public contract pages you are allowed to access. <br>
Risk: The skill includes optional server automation setup such as package installation, local scraper execution, and headless-browser avoidance techniques. <br>
Mitigation: Review and explicitly approve any sudo installation, local scraper process, or detection-avoidance setup before allowing the agent to run it. <br>
Risk: Explorer output may include decompiled code that does not compile directly or may differ from verified source. <br>
Mitigation: Treat fetched code as analysis material and verify it against official source or explorer labels before relying on it for development decisions. <br>


## Reference(s): <br>
- [Sui Decompile ClawHub page](https://clawhub.ai/EasonC13/sui-decompile) <br>
- [Suivision](https://suivision.xyz) <br>
- [Suivision package code view](https://suivision.xyz/package/{package_id}?tab=Code) <br>
- [Suiscan package contracts view](https://suiscan.xyz/mainnet/object/{package_id}/contracts) <br>
- [sui-move related skill](https://clawhub.ai/EasonC13/sui-move) <br>
- [sui-coverage related skill](https://clawhub.ai/EasonC13/sui-coverage) <br>
- [sui-agent-wallet related skill](https://clawhub.ai/EasonC13/sui-agent-wallet) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with browser workflow steps, JavaScript snippets, shell commands, and optional Puppeteer code.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide agents to save extracted modules as separate .move files.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
