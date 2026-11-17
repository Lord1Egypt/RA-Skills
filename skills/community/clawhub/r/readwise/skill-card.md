## Description:

Access Readwise highlights and Reader saved articles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[refrigerator](https://clawhub.ai/user/refrigerator)

### License/Terms of Use:


## Use Case:

Agents use this skill to help users retrieve Readwise books, highlights, exports, and Reader saved articles, and to save URLs into Reader when explicitly requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access Readwise account data such as highlights, notes, saved article metadata, and partial article content.

Mitigation: Install and run it only when that account access is intended, and treat returned JSON as potentially sensitive.

Risk: The Reader save command can add a URL to the user's Reader account.

Mitigation: Use the save command only for URLs the user explicitly intends to add to Reader.

Risk: API calls require a READWISE_TOKEN credential.

Mitigation: Provide the token through the documented environment variable and avoid exposing it in prompts, logs, or shared output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/refrigerator/skills/readwise)
- [Readwise](https://readwise.io)
- [Readwise access token](https://readwise.io/access_token)
- [Readwise Reader API](https://readwise.io/reader_api)
- [Readwise API](https://readwise.io/api_deets)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text]

**Output Format:** [Markdown instructions with shell command examples; invoked scripts return JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and READWISE_TOKEN.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
