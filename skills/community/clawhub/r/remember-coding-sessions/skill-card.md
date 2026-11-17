## Description:

Helps agents preserve coding-session continuity by storing and recalling architecture decisions, TODOs, and handoff notes through BlueColumn.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluecolumnconsulting-lgtm](https://clawhub.ai/user/bluecolumnconsulting-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to resume codebase work across sessions, record architecture decisions and TODOs, and prepare concise handoff notes for later work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Coding-session notes may be sent to the external BlueColumn service.

Mitigation: Avoid including secrets, credentials, customer data, proprietary source code, or sensitive internal details unless organizational policy approves that use.

Risk: The skill requires a BlueColumn API key for requests.

Mitigation: Store BLUECOLUMN_API_KEY in a secure environment variable or secrets manager.

## Reference(s):

- [BlueColumn API documentation](https://bluecolumn.ai/docs)
- [ClawHub skill page](https://clawhub.ai/bluecolumnconsulting-lgtm/skills/remember-coding-sessions)

## Skill Output:

**Output Type(s):** [guidance, shell commands]

**Output Format:** [Markdown guidance with inline bash curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BLUECOLUMN_API_KEY; produces API usage patterns and session-memory workflow guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
