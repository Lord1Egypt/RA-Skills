## Description:

Trader Simulator helps OpenClaw agents run multi-persona stock, crypto, and market discussion simulations for learning and practice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucasxing1](https://clawhub.ai/user/lucasxing1)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to practice stock and crypto market analysis conversations through simulated investor personas, multi-agent debates, and summarized viewpoints. It is for educational analysis workflows and should not be treated as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may auto-install external finance, search, and monitoring skills.

Mitigation: Review the dependency list before installation and use it only in environments where those tools are acceptable.

Risk: The MX/Eastmoney API key is a secret required by dependent finance and search skills.

Mitigation: Store the API key in the appropriate environment configuration and do not paste it into chat or source files.

Risk: Generated market commentary could be mistaken for investment advice.

Mitigation: Treat outputs as educational simulation content and independently verify market data before making financial decisions.

Risk: Automatic web, social, or stock-monitoring actions may retrieve broad external content or change watch settings.

Mitigation: Use the skill only where those lookups and monitoring changes are expected, and review outputs before acting on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lucasxing1/skills/trader-simulator)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands, configuration]

**Output Format:** [Markdown-style conversational analysis with command examples and risk warnings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use auto-installed finance, search, and stock monitoring skills when available.]

## Skill Version(s):

1.5.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
