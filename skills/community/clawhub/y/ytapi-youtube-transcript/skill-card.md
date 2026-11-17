## Description:

Retrieves YouTube transcripts and captions through YTAPI in text, Markdown, timestamped JSON, SRT, or VTT formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ytapi](https://clawhub.ai/user/ytapi)

### License/Terms of Use:

MIT-0

## Use Case:

People who share a YouTube video link or ID can use this skill to retrieve its captions for reading, summarizing, quoting, translating, or searching. It supports choosing a transcript language and output format through YTAPI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup saves the API key for future sessions without clearly explaining or limiting which sessions can access it.

Mitigation: Choose a storage method with clear access boundaries; prefer an existing connector, session-only credentials, or a scoped secret store.

Risk: Account signup shares the user's email with YTAPI, and successful transcript requests use account credits.

Mitigation: Use an email only if comfortable sharing it, and check credit use and pricing before making requests.

## Reference(s):

- [YTAPI documentation](https://docs.ytapi.dev)
- [YTAPI](https://ytapi.dev)
- [API key setup guide](references/auth-setup.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Subtitle files]

**Output Format:** [Plain text, Markdown, timestamped JSON, SRT, or VTT]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Transcript language and output format can be selected; successful requests consume YTAPI credits.]

## Skill Version(s):

1.2.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
