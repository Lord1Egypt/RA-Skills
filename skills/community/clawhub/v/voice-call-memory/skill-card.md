## Description:

Voice Call Memory helps voice agents store, summarize, and search caller history, topics, outcomes, and handoff notes across conversations using the BlueColumn API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluecolumnconsulting-lgtm](https://clawhub.ai/user/bluecolumnconsulting-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and voice-agent teams use this skill to persist structured call summaries, recall caller history when a call connects, and prepare handoff notes so callers do not need to repeat prior context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores identifiable voice-call details in an external memory service without enough stated privacy controls.

Mitigation: Use only where recording and storage are authorized, provide required notice or consent, minimize or redact phone numbers and sensitive details, and define retention, deletion, and access controls before real-call use.

Risk: Improper API-key or endpoint handling could expose caller memory or route call data to an unintended service.

Mitigation: Verify the BlueColumn/Supabase endpoint before use and keep the BlueColumn API key in a secret store or environment variable rather than embedding it in prompts, logs, or shared files.

## Reference(s):

- [BlueColumn API documentation](https://bluecolumn.ai/docs)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash code blocks and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a BlueColumn API key and produces API-call guidance for storing and recalling caller memory.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
