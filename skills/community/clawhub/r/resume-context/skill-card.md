## Description:

Resume Context helps OpenClaw answer questions about coding sessions, recent development work, and project notes by running the resume CLI and returning Redis-cached briefing output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nickleodoen](https://clawhub.ai/user/nickleodoen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical users use this skill to retrieve plain-English session briefings and project notes for local coding projects from resume CLI data. It is intended for OpenClaw environments with the resume CLI, Node.js, and a Redis connection configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent command capture can expose sensitive development activity from local coding sessions.

Mitigation: Inspect the resume shell hook before enabling it and use the skill only for repositories where session tracking is acceptable.

Risk: Developer-session output may flow through an LLM provider and Redis cache.

Mitigation: Avoid putting secrets in shell commands, prefer TLS Redis, and do not use the skill with sensitive repositories unless that data flow is acceptable.

Risk: The bridge executes a local resume binary and uses broad local project paths.

Mitigation: Install a trusted pinned resume version and verify RESUME_BIN and project paths before deployment.

## Reference(s):

- [ClawHub Resume Context Skill Page](https://clawhub.ai/nickleodoen/skills/resume-context)
- [resume CLI GitHub Repository](https://github.com/nickleodoen/resume)
- [Redis Cloud](https://cloud.redis.io/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON from the bridge with an output field containing plain-English briefing or notes text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include cache status, TTL, source command, and project path.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
