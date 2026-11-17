## Description:

Extract, summarize, and synthesize WeChat public account articles into structured knowledge cards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn public WeChat account articles, URL lists, shared text, or archived HTML into concise summaries, structured knowledge cards, and cross-article syntheses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may access URL-list files and output folders chosen by the user.

Mitigation: Grant access only to the specific input files and destination folders needed for the digest task.

Risk: Providing private articles, cookies, or account credentials could expose sensitive content or account access.

Mitigation: Use public articles only and do not provide cookies, credentials, or private article material unless a future version documents why they are needed and how they are protected.

Risk: Article summaries and extracted facts may omit context or include extraction errors.

Mitigation: Review generated summaries, key data, and quotes against the source article before relying on them for decisions or publication.

Risk: Republishing long excerpts from copyrighted articles may create rights concerns.

Mitigation: Use the skill for summaries and extracts rather than full-text republication, matching the artifact's stated safety posture.

## Reference(s):

- [WeChat Digest Output Formats Reference](artifact/references/formats.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, guidance]

**Output Format:** [Markdown summaries and JSON-style knowledge cards or cross-article synthesis objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write structured notes to stdout or files; summaries are intended as extracts rather than full-text republishing.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
