## Description: <br>
Knowledge base for the Superfluid Protocol and its ecosystem. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kasparkallas](https://clawhub.ai/user/kasparkallas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to answer Superfluid Protocol questions, choose the right contract, SDK, subgraph, or helper script reference, and produce implementation guidance for streams, pools, Super Apps, Super Tokens, automation, and protocol investigations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Protocol guidance can lead users toward token approvals, flow-operator permissions, EIP-712 signatures, relay providers, or on-chain contract interactions. <br>
Mitigation: Verify contract addresses from official sources, use capped allowances and granular flow limits, review signatures and transactions before execution, and revoke permissions when they are no longer needed. <br>
Risk: Helper scripts query external Superfluid data sources and package-provided metadata, so stale or unexpected upstream data could affect investigation results. <br>
Mitigation: Cross-check important balances, token addresses, network metadata, and subgraph results against official protocol sources before making production or financial decisions. <br>


## Reference(s): <br>
- [Protocol Architecture Guide](references/guides/architecture.md) <br>
- [SDK Guide](references/guides/sdks.md) <br>
- [Scripts Guide](references/guides/scripts.md) <br>
- [Super Apps Guide](references/guides/super-apps.md) <br>
- [Clear Macro Guide](references/guides/clear-macro.md) <br>
- [API Services Guide](references/guides/api-services.md) <br>
- [Protocol Subgraph Guide](references/subgraphs/protocol-v1-guide.md) <br>
- [GDA Scalability Deep Research](references/deep-researches/gda-scalability.md) <br>
- [Semantic Money Yellowpaper Deep Research](references/deep-researches/semantic-money-yellowpaper.md) <br>
- [Superfluid Reporter](https://reporter.superfluid.org) <br>
- [Super Token Listing](https://tokens.superfluid.org/listing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code blocks and JSON or shell command snippets when useful] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May point to artifact reference files and helper scripts for contract ABIs, selectors, metadata, token lists, and balances.] <br>

## Skill Version(s): <br>
1.2.4 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
