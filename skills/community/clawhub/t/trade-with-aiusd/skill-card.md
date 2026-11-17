## Description:

Manage AIUSD trading, staking, withdrawals, balance checks, gas top-ups, and transaction history via authenticated backend calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chaunceyliu](https://clawhub.ai/user/chaunceyliu)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to let an agent manage AIUSD account queries, trading, staking, withdrawals, gas top-ups, deposits, authentication recovery, and transaction history through authenticated AIUSD tooling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can initiate trades, staking, withdrawals, and gas-related actions through authenticated AIUSD tooling.

Mitigation: Require explicit transaction previews and confirmations outside the skill's wording rules before any financial action.

Risk: The installer can run npm scripts and replace an existing local aiusd-skill directory.

Mitigation: Review the installer and dependency installation behavior before running it, and install only in a directory where replacing aiusd-skill is acceptable.

Risk: Re-authentication can read local authentication token locations and clear local authentication caches.

Mitigation: Use re-authentication only when the account context is understood, and verify the active account after login completes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chaunceyliu/skills/trade-with-aiusd)
- [AIUSD official website](https://aiusd.ai)
- [AIUSD OAuth login](https://mcp.alpha.dev/oauth/login)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with inline shell commands and structured tool results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initiate high-impact financial actions through authenticated AIUSD tooling; require explicit transaction previews and confirmations outside the skill's wording rules.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact build-info.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
