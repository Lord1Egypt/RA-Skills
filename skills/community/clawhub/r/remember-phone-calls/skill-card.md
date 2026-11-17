## Description:

Remember Phone Calls helps agents store and recall phone-call context, including who called, why, outcomes, agreements, and follow-up promises, using the BlueColumn API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluecolumnconsulting-lgtm](https://clawhub.ai/user/bluecolumnconsulting-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

External-facing call-handling agents use this skill to preserve caller context, retrieve prior call history, and track commitments so follow-up conversations can continue from the latest known state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive phone-call details may be sent to BlueColumn's external backend.

Mitigation: Use the skill only where organizational policy allows external storage of call summaries and recall queries.

Risk: Secrets, payment data, health information, regulated identifiers, or sensitive personal details could be logged in call notes.

Mitigation: Instruct agents to avoid those data classes unless explicit approval, retention controls, and a deletion plan are in place.

Risk: Stored commitments and call history may persist longer than users expect.

Mitigation: Confirm the retention and deletion process before production use and document who can request removal.

## Reference(s):

- [BlueColumn API documentation](https://bluecolumn.ai/docs)
- [ClawHub skill page](https://clawhub.ai/bluecolumnconsulting-lgtm/skills/remember-phone-calls)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash curl commands and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BLUECOLUMN_API_KEY; sends call summaries, recall queries, tags, and follow-up notes to BlueColumn external endpoints.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
