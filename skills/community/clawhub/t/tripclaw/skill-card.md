## Description:

Imports OpenClaw-generated road trip itineraries into a user's TripClaw account via the TripClaw API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tripclaws](https://clawhub.ai/user/tripclaws)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect itinerary details from a conversation, structure them as TripClaw trip JSON, and import them into a TripClaw account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: TripClaw API keys can be exposed when supplied on the command line.

Mitigation: Set TRIPCLAW_API_KEY in the environment and avoid passing credentials with --api-key.

Risk: The bundled API reference documents broader account-changing operations than the import-only purpose requires.

Mitigation: Review the API reference and constrain agent use to trip import unless the user explicitly authorizes additional account operations.

Risk: Detailed itinerary data is sent to TripClaw during import.

Mitigation: Install and use the skill only when the user is comfortable sharing trip waypoints, accommodations, activities, and budget details with TripClaw.

## Reference(s):

- [TripClaw API Reference](artifact/references/api.md)
- [TripClaw Skill Page](https://clawhub.ai/tripclaws/skills/tripclaw)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke the TripClaw import script to send itinerary JSON to the TripClaw API when the user provides credentials and trip data.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
