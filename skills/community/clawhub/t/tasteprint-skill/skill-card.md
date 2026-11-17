## Description:

Use when a user asks for product, shopping, gift, gear, or purchase recommendations, or wants to build, update, inspect, sync, or delete a local Tasteprint preference profile.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zaodushi](https://clawhub.ai/user/zaodushi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to collect user-authorized preference signals into a local Tasteprint profile and apply those signals to product recommendations. It also supports profile management tasks such as updating, inspecting, syncing, and deleting the profile.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed to collect and persist sensitive shopping, content, and social-account signals.

Mitigation: Use only with explicit user consent, confirm authorized platforms and data ranges before collection, and keep profile storage local under the skill directory.

Risk: Required scoping reference files are missing from the artifact, increasing uncertainty around platform-specific collection and storage behavior.

Mitigation: Review the release before installing and do not perform authenticated collection unless the referenced files and selected browser provider guidance are present and verified.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zaodushi/skills/tasteprint-skill)
- [Server-resolved source repository](https://github.com/zaodushi/Tasteprint.skill)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Files, Shell commands, Guidance]

**Output Format:** [Markdown responses with JSON profile and raw-data files written under the skill directory]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include local preference profiles, task hypotheses, collection status envelopes, recommendation guidance, and profile-management instructions.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
