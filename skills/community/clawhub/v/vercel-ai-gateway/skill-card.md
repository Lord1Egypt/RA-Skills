## Description:

Helps agents discover Vercel AI Gateway models, compare pricing, inspect credits and usage, and run inference through an authorized Maton connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maton](https://clawhub.ai/user/maton)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other AI Gateway users can compare available models and costs, review account credits and usage, and request inference through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hosted functions, triggers, destinations, or watch commands can create ongoing automation or forward data.

Mitigation: Require explicit approval of the exact account, destination hosts, payload fields, and expected costs before enabling them.

Risk: Inference requests can incur charges and expose prompt content to the selected provider.

Mitigation: Confirm model and request size, check pricing, and avoid sending secrets or unnecessary sensitive data.

Risk: Generated responses may contain misleading or adversarial instructions.

Mitigation: Treat model output as untrusted and review it before using it in commands or downstream actions.

## Reference(s):

- [Maton](https://maton.ai)
- [Maton documentation](https://docs.maton.ai)
- [Vercel AI Gateway REST API](https://vercel.com/docs/ai-gateway/sdks-and-apis/rest-api)
- [Vercel AI Gateway models](https://vercel.com/ai-gateway/models)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown guidance with command examples and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Inference may incur usage charges.]

## Skill Version(s):

1.2.7 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
