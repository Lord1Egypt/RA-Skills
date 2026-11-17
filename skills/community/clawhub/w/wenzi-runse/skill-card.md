## Description:

Rewrites Chinese AI-generated text into a more natural human style using selectable flash, pro, and pro_plus processing modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abcqq1234567](https://clawhub.ai/user/abcqq1234567)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to process Chinese drafts of at least 300 characters when they explicitly request AI-trace removal, humanization, rewriting, polishing, or formatting. The agent runs the bundled script, returns the processed text from the service, and avoids rewriting the result itself.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Full user text is sent to a cloud service for processing.

Mitigation: Use the skill only for text that may be shared with that service, and avoid private, regulated, or proprietary drafts.

Risk: Personal API keys can be stored in plaintext local configuration.

Mitigation: Prefer one-time keys passed for a single run unless plaintext local storage is acceptable, and clear saved keys when they are no longer needed.

Risk: Broad trigger terms could cause processing when a user did not intend to submit text.

Mitigation: Confirm before processing pasted text unless the user clearly requests AI-trace removal, rewriting, polishing, formatting, or a specific processing tier.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abcqq1234567/skills/wenzi-runse)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [JSON from the script with success, result, and message fields; the agent delivers the returned rewritten text as plain text or Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a minimum 300-character input text and offers flash, pro, and pro_plus processing modes.]

## Skill Version(s):

1.6.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
