## Description:

Calculate vig (juice/overround/hold) for any sportsbook market, convert odds to no-vig fair lines, and rank books by efficiency.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rsquaredsolutions2026](https://clawhub.ai/user/rsquaredsolutions2026)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to calculate sportsbook vig, hold percentage, implied probabilities, and no-vig fair probabilities from user-provided American odds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake betting-odds arithmetic for betting or financial advice.

Mitigation: Use the skill only as a calculator for odds inputs; users remain responsible for decisions, legal compliance, and risk tolerance.

Risk: The skill relies on shell-executed Python snippets with user-provided odds.

Mitigation: Review commands before execution and provide only trusted numeric odds in a local environment with python3 installed.

## Reference(s):

- [Vig Calculator Skill Release](https://clawhub.ai/rsquaredsolutions2026/skills/vig-calculator)
- [AgentBets Vig Calculator Tutorial](https://agentbets.ai/guides/openclaw-vig-calculator-skill/)
- [OpenClaw Skills Series](https://agentbets.ai/guides/#openclaw-skills)
- [Agent Betting Stack](https://agentbets.ai/guides/agent-betting-stack/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with inline Python shell commands and calculated numeric results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and performs local arithmetic on user-provided odds.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
