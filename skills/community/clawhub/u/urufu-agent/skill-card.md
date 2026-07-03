## Description: <br>
Play urufu g\u0113mu on Base with your AI agent -- check portfolio, claim yield, gasless mint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[urufu-labs](https://clawhub.ai/user/urufu-labs) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to let an AI agent monitor a Urufu wallet on Base, preview claim or mint eligibility, and run explicit user-approved claim, mint, paid mint, or meadow play commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent environment to hold wallet-signing material. <br>
Mitigation: Use a dedicated low-value wallet or scoped session key, never use a main wallet private key, keep secrets out of chat and shell history, and rotate any key that was exposed. <br>
Risk: The paid mint path can spend ETH or URU from the configured wallet. <br>
Mitigation: Run previews before any paid mint, require explicit user approval for paid writes, and keep only limited funds in the signing wallet. <br>
Risk: Relay and wallet actions can be abused by repeated or automated requests. <br>
Mitigation: Respect the skill's read-only default, explicit write commands, claim and mint cooldowns, retry backoff, and zero-yield or dust-claim skips. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/urufu-labs/skills/urufu-agent) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/urufu-labs) <br>
- [OpenClaw metadata homepage](https://github.com/urufu-labs/urufu-agent) <br>
- [Agent play guide](docs/agent-play.md) <br>
- [OpenAPI specification](docs/api/openapi.yaml) <br>
- [Steward CLI guide](scripts/README.md) <br>
- [Bootstrap prompt](references/BOOTSTRAP.md) <br>
- [Onboarding guide](references/onboarding.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON snippets, and agent-facing instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May trigger CLI commands and API calls when the user explicitly approves wallet actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
