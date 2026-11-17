## Description:

This skill helps agents use XinJianXue's Long-Distance Relationship Advisor workflow for consent-gated relationship analysis, account onboarding, API calls, and human-facing guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weixin97676414](https://clawhub.ai/user/weixin97676414)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill when they explicitly want XinJianXue long-distance relationship analysis and guidance about maintenance cost, communication patterns, and whether to continue or close the distance. Agents use it to confirm consent, collect required personal details, manage service onboarding, call the XinJianXue API, and translate the returned report into user-facing guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the user for a sensitive one-time authorization code that binds the user's account to the agent.

Mitigation: Use the official XinJianXue domain and a host secret-entry or browser-based flow when available; treat the code as sensitive, single-use, and never reusable after binding.

Risk: The skill stores persistent license_key and api_key credentials after onboarding.

Mitigation: Agree on a dedicated credential store before onboarding, prefer environment variables or an OS keychain, and never place credentials in chat, long-term memory, notes, or configuration files.

Risk: The skill sends personal birth, gender, and location details to the XinJianXue API and spends account tokens for report calls.

Mitigation: Require explicit user consent before each analysis, collect only the required details, disclose token usage, and avoid analyzing third parties without clear mention and agreement.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/weixin97676414/skills/xinjianxue-skill-long-distance-global)
- [XinJianXue website](https://www.xinjianxue.com)
- [XinJianXue API base](https://www.xinjianxue.com/api/xinjianxue)

## Skill Output:

**Output Type(s):** [text, guidance, configuration]

**Output Format:** [Markdown or plain text guidance with HTTP request details when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user confirmation before analysis, uses persistent service credentials after onboarding, and consumes account tokens for report calls.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
