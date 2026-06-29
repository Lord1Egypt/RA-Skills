## Description: <br>
Installs and sets up the Refacil Pay CLI, then guides the agent to install the package's operating skill for Colombian payment workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[erikole21](https://clawhub.ai/user/erikole21) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to install refacil-pay-cli, read the package's AGENTS.md contract, and configure the operating skill in their agent environment. It is a bootstrap skill only and does not itself execute payments. <br>

### Deployment Geography for Use: <br>
Global, with payment workflows focused on Colombia. <br>

## Known Risks and Mitigations: <br>
Risk: Installing this skill adds a payments integration and delegates ongoing operation to an npm package and its installed operating skill. <br>
Mitigation: Review the package AGENTS.md and installed operating skill, and verify that refacil-pay-cli is the intended package before use. <br>
Risk: Payment authentication could expose credentials if handled directly in an agent session. <br>
Mitigation: Authenticate through the browser or device page, never type or store passwords in the agent, and do not run login --console on the user's behalf. <br>
Risk: Cash-in, cash-out, or payment-link commands could move money if run without clear authorization. <br>
Mitigation: Require explicit user confirmation in chat before any payment or cash movement command, especially commands using --yes. <br>


## Reference(s): <br>
- [refacil-pay-cli npm package](https://www.npmjs.com/package/refacil-pay-cli) <br>
- [Refacil Pay Setup on ClawHub](https://clawhub.ai/erikole21/refacil-pay-setup) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides setup commands and handoff guidance; payment operations remain governed by the installed operating skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
