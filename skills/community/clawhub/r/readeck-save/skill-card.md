## Description:

Save articles to Readeck (self-hosted read-it-later app). Use when the user wants to save an article for later reading, add something to their reading list, or send a page to Readeck.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nickian](https://clawhub.ai/user/nickian)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to send article URLs to a configured self-hosted Readeck instance for later reading.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved URLs are sent to the configured Readeck server, which will fetch and process the linked page.

Mitigation: Install and use the skill only with a Readeck instance you trust, and avoid saving sensitive internal or authenticated URLs unless that is intended.

Risk: The skill requires a Readeck API token for bookmark creation.

Mitigation: Use a minimally scoped token where possible and keep the token in the configured environment rather than sharing it in prompts or saved content.

Risk: The artifact script posts the URL in JSON without explicit JSON encoding.

Mitigation: Review or update the script to JSON-encode the URL before posting, especially before handling unusual URLs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nickian/skills/readeck-save)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a configured Readeck URL and bearer token to submit a user-provided URL.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
