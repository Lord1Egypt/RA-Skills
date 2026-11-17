## Description:

Tracks local SMB client onboarding records, checklist status, and optional LLM-generated reminder text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jzargona](https://clawhub.ai/user/jzargona)

### License/Terms of Use:

MIT-0

## Use Case:

Agencies, consultants, and freelancers use this skill to record client onboarding details, track pending steps, configure reminders, and draft reminder text for manual review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Client names, contact emails, contract values, and onboarding status may be confidential and are stored locally in plaintext.

Mitigation: Use the skill only with client data approved for local plaintext storage, and review local files under ~/.openclaw/smb-client-onboarding/ according to your retention policy.

Risk: Optional LLM reminder generation can send reminder-generation context, including contact email in the current implementation, to MiniMax.

Mitigation: Avoid setting MINIMAX_API_KEY unless MiniMax processing is acceptable for the client data, and review generated reminders before manual sending.

## Reference(s):

- [SMB Client Onboarding Reference Docs](references/README.md)
- [SMB Client Onboarding ClawHub Listing](https://clawhub.ai/jzargona/skills/smb-client-onboarding)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands and plaintext reminder drafts; local JSON files for records and configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores onboarding and configuration data locally under ~/.openclaw/smb-client-onboarding/; optional reminder generation can call MiniMax when MINIMAX_API_KEY is set.]

## Skill Version(s):

1.0.1 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
