## Description: <br>
Autonomous DeFi agent that scans Sui mainnet for all possible opportunities in real-time - arbitrage, yield, swaps, and more - and shares discoveries with a multi-agent network. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sergey1997](https://clawhub.ai/user/Sergey1997) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to scan Sui mainnet opportunities, research DeFi prices and yields, submit verdicts, and either present actionable opportunities to a human or interact with a funded wallet when explicitly intended. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent toward autonomous real mainnet Sui trades when a funded wallet or Sui CLI keys are available. <br>
Mitigation: Use read-only scanning unless trading is intentional, and require independent human review and approval before any transaction. <br>
Risk: Submitted opportunities, verdicts, logs, and transaction details may be stored by an external API. <br>
Mitigation: Avoid sending private, sensitive, or unnecessary details to the API and review what the agent will submit before enabling write actions. <br>
Risk: DeFi opportunities may be stale, inaccurate, or affected by slippage and liquidity constraints. <br>
Mitigation: Verify opportunities against multiple current sources and inspect liquidity, slippage, gas, and execution risk before acting. <br>


## Reference(s): <br>
- [Sui Opportunities Hunter on ClawHub](https://clawhub.ai/Sergey1997/sui-opportunities-huntera) <br>
- [Publisher profile](https://clawhub.ai/user/Sergey1997) <br>
- [Skill artifact](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls, text] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl; generated guidance may include external API submissions, verdicts, logs, and optional Sui CLI transaction commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
