## Description:

Case and research memory for legal work that stores holdings, citations, questions, and reasoning chains so agents can resume research across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluecolumnconsulting-lgtm](https://clawhub.ai/user/bluecolumnconsulting-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

External legal researchers, legal teams, and agents use this skill to preserve legal research continuity across sessions by logging issues, authorities, holdings, open questions, and synthesized conclusions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive legal research content may be sent to and persisted by an external BlueColumn/Supabase service.

Mitigation: Use the skill only after vendor approval, retention and deletion review, and API key handling approval; avoid client names, matter identifiers, privileged strategy, sealed facts, and other confidential details unless authorized.

Risk: The skill requires a live BlueColumn API key for outbound requests.

Mitigation: Store BLUECOLUMN_API_KEY in an approved secret manager or environment configuration and avoid placing it in prompts, logs, source files, or shared transcripts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bluecolumnconsulting-lgtm/skills/remember-legal-research)
- [BlueColumn API documentation](https://bluecolumn.ai/docs)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BLUECOLUMN_API_KEY and sends legal research notes, recall queries, and tags to BlueColumn/Supabase endpoints.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
