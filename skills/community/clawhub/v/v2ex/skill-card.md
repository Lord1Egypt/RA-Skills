## Description:

V2EX API 2.0 integration for accessing V2EX forum data, notifications, topics, nodes, and member profiles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[timqian](https://clawhub.ai/user/timqian)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to guide agents in working with the V2EX API for forum notifications, topics, nodes, member profiles, token checks, and example client code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide an agent to use a V2EX Personal Access Token.

Mitigation: Store the token outside code, use the least-privileged token available, and avoid exposing it in prompts, logs, or committed files.

Risk: The documented V2EX API workflows include deleting notifications.

Mitigation: Require explicit user confirmation before performing delete operations.

Risk: API use can exceed V2EX rate limits.

Mitigation: Check rate limit headers, apply backoff, and cache responses where appropriate.

## Reference(s):

- [V2EX skill page](https://clawhub.ai/timqian/skills/v2ex)
- [V2EX API Documentation](https://www.v2ex.com/help/api)
- [Personal Access Tokens](https://www.v2ex.com/settings/tokens)
- [V2EX API Node](https://www.v2ex.com/go/v2ex-api)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline HTTP, bash, and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe authenticated API calls that require a V2EX Personal Access Token.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
