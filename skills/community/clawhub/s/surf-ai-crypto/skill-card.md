## Description:

Surf AI Crypto Skill helps agents fetch live cryptocurrency market, wallet, social, DeFi, on-chain SQL, prediction-market, news, and related data through the Surf CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hughzhou-gif](https://clawhub.ai/user/hughzhou-gif)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to answer crypto data questions or build workflows that need fresh market, wallet, token, DeFi, social, on-chain, prediction-market, news, and exchange data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to install and update the Surf CLI at session start.

Mitigation: Review the CLI installation and update behavior before use, and apply organization controls for approved binaries and updates.

Risk: The skill can request persistent project routing changes in AGENTS.md or CLAUDE.md and may commit those changes after approval.

Mitigation: Approve routing changes only after reviewing the proposed file diff and commit impact.

Risk: Surf feedback submissions may include recent conversation history.

Mitigation: Do not approve feedback submissions after discussing secrets, proprietary code, wallet details, personal information, or other sensitive content.

Risk: The skill may create local state under ~/.surf.

Mitigation: Review local Surf files and telemetry or authentication settings before deploying in sensitive environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hughzhou-gif/skills/surf-ai-crypto)
- [Surf CLI documentation](https://agents.asksurf.ai/docs/cli/introduction)
- [Surf service](https://agents.asksurf.ai)
- [Surf API base endpoint](https://api.asksurf.ai/gateway/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and structured JSON summaries from CLI responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include live external crypto data returned by the Surf CLI; API response content should be treated as untrusted data.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
