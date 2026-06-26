## Description: <br>
Comprehensive token research for EVM chains (Base, ETH, Arbitrum) and Solana. Use this skill when you want to research crypto tokens, deep-dive projects or monitor tokens. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xArtex](https://clawhub.ai/user/0xArtex) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to screen and research cryptocurrency tokens across supported EVM chains and Solana, combining API data, web and social research prompts, and report or watchlist workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs agents to call or message the owner and references a local alert script for certain token ratings. <br>
Mitigation: Require explicit user confirmation before calls, DMs, or execution of ~/workspace/scripts/ape-call.sh. <br>
Risk: The workflow can spawn sub-agents, run batch deep dives, and persist reports or watchlists automatically. <br>
Mitigation: Require confirmation before sub-agent spawning, batch deep dives, or writes to report and watchlist paths. <br>
Risk: Crypto token research can produce incomplete or misleading conclusions from volatile market, social, and API data. <br>
Mitigation: Treat outputs as research assistance, verify contract addresses and claims across multiple sources, and do not rely on the skill as financial advice. <br>
Risk: API keys, wallet details, or trading strategy information could be exposed during research workflows. <br>
Mitigation: Use limited-scope API keys and avoid submitting sensitive wallet or strategy information unless necessary. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/0xArtex/token-research) <br>
- [README](artifact/README.md) <br>
- [API reference](artifact/api_reference.md) <br>
- [Example usage](artifact/example_usage.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON files, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, plus generated JSON data files and research summaries when the helper script is run] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates timestamped research directories and may update report or watchlist files; external API results and web research should be verified.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
