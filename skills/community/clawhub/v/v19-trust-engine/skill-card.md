## Description:

V19 Trust Engine documents a trust-scoring and certification workflow for agents, including weighted trust dimensions, VPAV validation, score thresholds, decay behavior, and registration calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuyanfeng1234](https://clawhub.ai/user/liuyanfeng1234)

### License/Terms of Use:

MIT-0

## Use Case:

External agent developers and operators use this skill to understand and test a V19 trust-score certification workflow, including registration, recurring audit calls, VPAV validation, and score decay.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users to register and make recurring trust calls through an unaudited temporary external service with unclear data and key handling.

Mitigation: Do not send sensitive agent names, production identifiers, private audit data, or long-lived keys unless service ownership, stable domain, privacy and retention terms, and credential rotation and revocation procedures are verified.

Risk: The documented workflow depends on external governance endpoints and an example public key.

Mitigation: Review endpoint ownership and expected data handling before using the workflow with real agents or production audit data.

## Reference(s):

- [V19 Trust Engine on ClawHub](https://clawhub.ai/liuyanfeng1234/skills/v19-trust-engine)
- [V19 Trust Manifesto](https://clawhub.com/skills/v19-trust-manifesto)
- [V19 Certified Agent Workflow](https://clawhub.com/skills/v19-certified-agent-workflow)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with tables and bash curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance; includes external governance endpoints and an example public key.]

## Skill Version(s):

1.0.0 (source: frontmatter and server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
