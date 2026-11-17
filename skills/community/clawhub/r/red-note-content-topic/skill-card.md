## Description:

AI-powered Xiaohongshu (RED) topic planner that generates trending topic ideas and headline directions based on account positioning and target audience.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wsd-mj](https://clawhub.ai/user/wsd-mj)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, marketers, and social media operators use this skill to request Xiaohongshu topic and headline ideas tailored to an account direction and optional audience profile.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on wsdsocial.com's hosted API and sends the provided account positioning and audience details to that service.

Mitigation: Install only if you trust the hosted service, and avoid submitting confidential strategy, private customer data, or personal information.

Risk: The WSD_API_KEY credential could be exposed if copied into prompts, logs, shell history, or shared configuration.

Mitigation: Store WSD_API_KEY as a secret environment variable and do not include it in public logs, examples, or shared transcripts.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/wsd-mj/skills/red-note-content-topic)
- [Publisher profile](https://clawhub.ai/user/wsd-mj)
- [Server-resolved source repository](https://github.com/WSD-MJ/red-note-content-topic)
- [WSD Social skill key setup](https://ai.wsdsocial.com/skills)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Remote API response with topic suggestions and headline ideas]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WSD_API_KEY and sends the provided account direction and optional audience profile to wsdsocial.com's hosted API.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
