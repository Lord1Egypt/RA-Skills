## Description:

Voice Memory gives voice and phone agents BlueColumn-backed memory for callers, meetings, coaching sessions, sales calls, and journal entries, and requires a BlueColumn API key (bc_live_*).

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluecolumnconsulting-lgtm](https://clawhub.ai/user/bluecolumnconsulting-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and voice-agent builders use this skill to store and recall conversation memory for callers, meetings, coaching sessions, sales calls, and journal entries through BlueColumn. It is intended for agents that need continuity across calls and can provide a BlueColumn API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive call details may be stored in an external memory service without enough documented privacy, retention, or scoping controls.

Mitigation: Use only where callers have been informed and consent to external memory storage; confirm retention, deletion, tenant isolation, endpoint details, and approval for sensitive or regulated data before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bluecolumnconsulting-lgtm/skills/voice-memory)
- [Publisher profile](https://clawhub.ai/user/bluecolumnconsulting-lgtm)
- [BlueColumn](https://bluecolumn.ai)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent instructions for storing and recalling voice-memory records with an external BlueColumn service.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
