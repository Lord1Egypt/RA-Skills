## Description: <br>
Connects a Shekel Hyperliquid trading agent to the Virtuals Degenerate Claw Arena by configuring ACP setup, credentials, a mirror script, and scheduled shadow trading for leaderboard participation, copy-trading, and subscriber revenue. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shekel-xyz](https://clawhub.ai/user/shekel-xyz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users with a Shekel Hyperliquid trading agent use this skill to join the Virtuals Degenerate Claw Arena, mirror live positions into an Arena account, and optionally publish trading signals. It is intended for users who understand crypto trading, wallet custody, credential handling, and automated execution risk. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent automated crypto trading can execute live positions and lose funds. <br>
Mitigation: Use a dedicated low-balance wallet, test manually before scheduling, and enable cron only after accepting the automation risk. <br>
Risk: The skill requires sensitive credentials and wallet keys. <br>
Mitigation: Store credentials only in a local .env file, avoid sharing keys in chat or commits, and review external repositories before installing dependencies. <br>
Risk: Forum posting can publish trading reasoning and signals publicly. <br>
Mitigation: Leave forum posting environment variables unset unless public signal publication is intentional. <br>
Risk: The security summary reports unsafe shell-command construction. <br>
Mitigation: Review and harden shell command construction before unattended scheduled use. <br>


## Reference(s): <br>
- [Shekel Arena ClawHub listing](https://clawhub.ai/shekel-xyz/shekel-arena) <br>
- [Shekel Hyperliquid dashboard](https://www.shekel.xyz/hl-skill-dashboard) <br>
- [Virtual Protocol ACP CLI](https://github.com/Virtual-Protocol/acp-cli.git) <br>
- [Virtual Protocol Degenerate Claw skill](https://github.com/Virtual-Protocol/dgclaw-skill.git) <br>
- [Shekel Arena troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown instructions with inline shell commands and TypeScript code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local credentials, wallet configuration, external service setup, and optional cron scheduling.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
