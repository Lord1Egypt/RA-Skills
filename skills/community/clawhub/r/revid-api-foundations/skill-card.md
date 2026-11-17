## Description:

Foundation knowledge for every Revid skill: auth, the single render endpoint, the workflow discriminator, polling, webhooks, and the response envelope.

This skill is ready for commercial/non-commercial use.

## Publisher:

[api00](https://clawhub.ai/user/api00)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this foundation when composing Revid API calls, selecting workflows, configuring authentication, polling render status, and handling common failures for video generation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: REVID_API_KEY can grant access to Revid API usage.

Mitigation: Keep the key private, read it from configuration, and avoid exposing it in prompts, logs, or shared outputs.

Risk: Render calls may send scripts, URLs, media, or other source material to Revid.

Mitigation: Avoid sensitive source material unless the user accepts processing by Revid.

Risk: High-quality renders or credit purchases can spend credits.

Mitigation: Require explicit approval before actions that spend or purchase credits, and estimate credits before expensive renders.

## Reference(s):

- [Revid Public API v3 spec](https://documenter.getpostman.com/view/36975521/2sBXcGEfaB)
- [ClawHub skill page](https://clawhub.ai/api00/skills/revid-api-foundations)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls]

**Output Format:** [Markdown with HTTP examples, JSON snippets, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REVID_API_KEY for live Revid API use.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
