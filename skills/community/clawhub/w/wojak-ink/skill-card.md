## Description: <br>
Browse, search, analyze, and track Wojak Farmers Plot NFTs with floor prices, rarity estimates, price trends, traits, listings, and deal opportunities on the Chia blockchain. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Koba42Corp](https://clawhub.ai/user/Koba42Corp) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to query Wojak Farmers Plot NFT market data, inspect listings and character types, estimate rarity, and track local price history from public APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market, rarity, and deal outputs are informational estimates and may be incomplete or stale. <br>
Mitigation: Review source marketplace data before making trading decisions and treat rarity or deal calculations as advisory. <br>
Risk: The skill contacts public NFT APIs and depends on their availability and returned data quality. <br>
Mitigation: Expect API failures or outdated listings and re-run commands when fresh market data is required. <br>
Risk: Price tracking stores local market-history JSON files. <br>
Mitigation: Delete the skill's data directory when retained local history is no longer wanted. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Koba42Corp/wojak-ink) <br>
- [Koba42Corp ClawHub profile](https://clawhub.ai/user/Koba42Corp) <br>
- [Wojak.ink collection website](https://wojak.ink) <br>
- [MintGarden API](https://api.mintgarden.io) <br>
- [Dexie API](https://api.dexie.space/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance, JSON files] <br>
**Output Format:** [Plain text responses for CLI or chat channels, with local JSON history files when tracking is used] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public NFT APIs, caches marketplace data briefly, and can retain local market-history JSON files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
