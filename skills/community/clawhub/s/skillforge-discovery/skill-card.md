## Description:

SkillForge API 服务发现 detects OpenClaw Agent capability gaps, discovers matching paid AI API services, and returns selected service results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leongfans](https://clawhub.ai/user/leongfans)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to detect when a task needs an external paid API, discover matching SkillForge services, and return selected invocation results with cost information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task data and API credentials can be sent to a configurable external SkillForge endpoint.

Mitigation: Use only a trusted HTTPS platform URL and a narrowly scoped, revocable API key.

Risk: Paid service invocation can spend account balance without the skill itself enforcing the documented confirmation gate.

Mitigation: Require host-level per-call confirmation that shows the service, destination, data being sent, and authoritative price; also set external spending limits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leongfans/skills/skillforge-discovery)
- [Publisher profile](https://clawhub.ai/user/leongfans)
- [README.md](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, API calls, configuration, guidance]

**Output Format:** [JSON objects with human-readable text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js plus SKILLFORGE_API_URL and SKILLFORGE_API_KEY; paid invocations may return billing metadata.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
