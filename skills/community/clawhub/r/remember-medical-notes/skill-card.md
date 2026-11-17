## Description:

Private, authorized health-appointment memory for care continuity. Use when an agent tracks appointments, symptoms, and provider instructions for an authorized user, with consent and confidentiality built in. Requires a BlueColumn API key (bc_live_*).

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluecolumnconsulting-lgtm](https://clawhub.ai/user/bluecolumnconsulting-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

Authorized users and their agents use this skill to record health appointment notes, symptom timelines, medication changes, and provider instructions, then recall them before future visits. It is intended for care-continuity workflows where consent, confidentiality, and private tagging are required.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may send sensitive medical notes to an external Supabase API without enough disclosed data-handling detail.

Mitigation: Use only after confirming the endpoint, storage location, access controls, retention policy, deletion process, and token permissions with BlueColumn.

Risk: Unauthorized or excessive disclosure of health information could occur if notes are stored without clear user consent or private tagging.

Mitigation: Store only user-authorized information, tag entries as private, and avoid including health details that are not needed for the user's care-continuity task.

## Reference(s):

- [BlueColumn API documentation](https://bluecolumn.ai/docs)
- [ClawHub skill page](https://clawhub.ai/bluecolumnconsulting-lgtm/skills/remember-medical-notes)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BLUECOLUMN_API_KEY for API calls; generated notes may contain sensitive medical information.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
