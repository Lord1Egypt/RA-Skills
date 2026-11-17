## Description:

Token Tracker Pro tracks OpenClaw session token usage with daily, weekly, and cumulative statistics and provides token-saving suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[longziruo-max](https://clawhub.ai/user/longziruo-max)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to monitor local token consumption, review historical usage, export or clean usage data, and receive cost-saving model recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores local token history that may include session identifiers.

Mitigation: Install only when local storage of token usage history is acceptable, and review or minimize stored history before sharing the environment.

Risk: The security evidence reports under-disclosed persistent system changes related to shortcut setup.

Mitigation: Avoid running shortcut setup until autostart and shell profile changes are clearly disclosed and acceptable.

Risk: The security evidence reports dashboard exposure of sensitive local usage history.

Mitigation: Avoid running the dashboard until it is bound to localhost with authentication or field minimization appropriate for the environment.

Risk: The security guidance calls out shell-based npx execution, unpinned browser dependencies, and reset behavior that may not accurately delete data.

Mitigation: Review shell execution paths, pin or bundle browser dependencies, and verify data deletion behavior before deployment.

## Reference(s):

- [Token Tracker Pro Skill Definition](artifact/SKILL.md)
- [Quickstart](artifact/QUICKSTART.md)
- [Integration Guide](artifact/INTEGRATION.md)
- [Smart Recommendation Guide](artifact/SMART-RECOMMENDATION.md)
- [Release Changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with command examples, TypeScript integration snippets, CLI text output, and local dashboard views]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local token usage summaries, history exports, cleanup/reset commands, dashboard launch instructions, and model cost recommendations.]

## Skill Version(s):

2.2.0 (source: server release metadata and SKILL.md; package.json lists 2.1.0 and CHANGELOG top entry lists 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
