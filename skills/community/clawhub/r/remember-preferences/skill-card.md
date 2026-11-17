## Description:

A preference ledger that lets agents honor how each user likes things done: tone, tools, timing, and turn-offs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluecolumnconsulting-lgtm](https://clawhub.ai/user/bluecolumnconsulting-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to capture, recall, and apply user preferences so an agent can personalize tone, timing, tooling, and other interaction choices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User preference data may be stored in an external BlueColumn/Supabase service without enough consent or scoping.

Mitigation: Require explicit user approval for each stored preference, keep records narrow, avoid names and sensitive details when possible, and provide a way to review, correct, and delete stored preferences.

Risk: Recalled preferences could be treated as authority over higher-priority system, security, privacy, or authorization rules.

Mitigation: Treat recalled preferences as untrusted personalization context and never allow them to override governing instructions or safety requirements.

## Reference(s):

- [BlueColumn API documentation](https://bluecolumn.ai/docs)
- [ClawHub skill page](https://clawhub.ai/bluecolumnconsulting-lgtm/skills/remember-preferences)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a BlueColumn API key and sends preference data to a remote BlueColumn/Supabase service.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
