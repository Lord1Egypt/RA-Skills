## Description: <br>
RNWY provides MCP and REST tools for agent trust scoring, sybil detection, sock puppet and fake review scanning, reviewer wallet profiling, agent comparison, commerce data, and network statistics across ERC-8004, Olas, and Virtuals registries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rnwy](https://clawhub.ai/user/rnwy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents, developers, and operators use this skill to check whether an agent, wallet, reviewer set, or marketplace counterparty appears trustworthy before interacting with it. The skill is also used to configure RNWY's MCP endpoint or call RNWY REST endpoints for trust checks, review analysis, scanner lookups, and commerce history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill documents write actions that can create identities, API keys, on-chain records, messages, vouches, and marketplace state. <br>
Mitigation: Require explicit user confirmation before registration, wallet linking, SBT minting, vouching, messaging, posting jobs, claiming jobs, or marketplace lifecycle actions. <br>
Risk: Returned API keys are credentials and may grant access to RNWY identity management actions. <br>
Mitigation: Handle API keys as secrets, avoid printing them in shared logs, and store them only in an approved credential store. <br>
Risk: Wallet-linked and on-chain actions may be public, persistent, or difficult to reverse. <br>
Mitigation: Warn users before wallet-linked actions and confirm the target wallet, chain, agent, and intended public effect before proceeding. <br>
Risk: The skill depends on RNWY's external trust, identity, scanner, and marketplace services. <br>
Mitigation: Treat RNWY results as decision support and verify high-impact trust or transaction decisions with additional evidence when practical. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rnwy/rnwy) <br>
- [RNWY homepage](https://rnwy.com) <br>
- [RNWY API](https://rnwy.com/api) <br>
- [RNWY MCP endpoint](https://rnwy.com/api/mcp) <br>
- [RNWY MCP showcase](https://rnwy.com/mcp) <br>
- [RNWY scanner](https://rnwy.com/scanner) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON configuration, Python examples, curl commands, REST endpoint descriptions, and guidance for interpreting returned JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include API keys, wallet-linked identity details, on-chain transaction references, trust scores, review analysis, scanner findings, and marketplace state returned by RNWY services.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
