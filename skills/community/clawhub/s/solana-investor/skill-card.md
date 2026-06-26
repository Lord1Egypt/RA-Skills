## Description: <br>
Solana Investor coordinates portfolio, DCA, alert, and market sub-skills for multi-step Solana investment requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liji3597](https://clawhub.ai/user/liji3597) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users managing Solana investments use this skill to coordinate multi-step workflows across portfolio review, market checks, DCA setup, and price alerts. The skill is intended for requests that require multiple sub-skills, with confirmation before write actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package includes executable diagnostic scripts beyond the documented prompt workflow. <br>
Mitigation: Review or remove the scripts before use, and only run them after confirming which shared database, metrics, environment, signer, and compliance-file state they inspect. <br>
Risk: The skill coordinates investment-related workflows that may include write actions such as DCA strategy creation or alert setup. <br>
Mitigation: Require explicit user confirmation for each write action and keep read-only checks separate from state-changing operations. <br>
Risk: One sub-skill failure could otherwise obscure partial results in a multi-step investment workflow. <br>
Mitigation: Report each sub-step separately and continue presenting successful read results when another sub-step fails. <br>


## Reference(s): <br>
- [Solana Investor release page](https://clawhub.ai/liji3597/solana-investor) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands] <br>
**Output Format:** [Markdown text with structured workflow steps and referenced script commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Coordinates sub-skill calls and asks for confirmation before write operations.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata); artifact frontmatter reports 1.0.0 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
