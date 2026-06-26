## Description: <br>
Expose the Teller delta-neutral + lending Model Context Protocol server so agents can fetch opportunities, borrow terms, and on-chain transaction builders for Teller. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rbcp18](https://clawhub.ai/user/rbcp18) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to install, run, or update a Teller MCP server that exposes lending pool discovery, delta-neutral opportunity lookup, borrow term calculation, and borrow or repayment transaction builders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Borrow and repayment tools can return ready-to-submit transaction calldata that could affect real funds if signed automatically. <br>
Mitigation: Require manual wallet review before signing, including chain ID, target address, token approvals, amounts, loan terms, and configured API endpoint. <br>


## Reference(s): <br>
- [Teller Delta-Neutral + Lending API Cheat Sheet](references/delta-neutral-api.md) <br>
- [Teller Delta-Neutral API Reference](https://registry.scalar.com/@teller/apis/delta-neutral/latest) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance plus MCP tool responses with text summaries and structured JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include ready-to-submit borrow and repayment transaction payloads that require wallet review before signing.] <br>

## Skill Version(s): <br>
0.1.6 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
