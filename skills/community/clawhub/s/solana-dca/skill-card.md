## Description: <br>
Creates and manages simulated dollar-cost averaging strategies for Solana tokens, including setup, listing, pausing, and resuming strategy records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liji3597](https://clawhub.ai/user/liji3597) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agent operators use this skill to guide creation and management of simulated Solana token DCA strategies. It helps collect token, amount, frequency, and strategy ID inputs before running the matching command-line workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may mistake the workflow for live on-chain trading. <br>
Mitigation: State before first use that the DCA feature is simulated and records strategies without executing on-chain swaps. <br>
Risk: Incorrect token, amount, frequency, or strategy ID can create, pause, or resume the wrong simulated strategy record. <br>
Mitigation: Confirm token, amount, frequency, and strategy ID with the user before running create, pause, or resume commands. <br>
Risk: Actions can be attributed to the wrong account if the runtime supplies an incorrect user ID. <br>
Mitigation: Ensure the runtime supplies the authenticated user ID automatically before approving create, pause, or resume actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liji3597/solana-dca) <br>
- [Publisher profile](https://clawhub.ai/user/liji3597) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, text, configuration] <br>
**Output Format:** [Markdown-style guidance with inline shell commands and command-line text or JSON responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and SOLANA_NETWORK; scripts manage simulated strategy records.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
