## Description:

Summarizes important family-related mobile notifications by person, grouping children, spouse, parents or elders, and marking action-required versus FYI items.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vivalavida-say-hi](https://clawhub.ai/user/vivalavida-say-hi)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to turn recent mobile notifications into a family-focused digest grouped by relevant people. It helps surface requests, deadlines, and FYI updates from spouses, elders, schools, teachers, and other family contacts while filtering unrelated noise.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read sensitive phone notification files and infer family relationships from names and message content.

Mitigation: Install only when comfortable with that access, and use specific people or date ranges when requesting a digest.

Risk: Broad trigger phrases may cause the skill to review notifications for less-specific family-message requests.

Mitigation: Use narrow prompts for the person or time window of interest and avoid broad requests when unrelated notifications should not be reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vivalavida-say-hi/skills/yoooclaw-family-digest)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown-formatted conversational summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Groups by inferred family member and includes importance labels, sources, deadlines, and action items when present.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
