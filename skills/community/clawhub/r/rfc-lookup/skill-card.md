## Description:

Look up IETF RFCs and read what a specification actually says.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shbernal](https://clawhub.ai/user/shbernal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical writers use this skill to locate current IETF standards, verify protocol requirements, and cite relevant sections without reading an entire RFC.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional offline corpus and index downloads are large and persist locally; corpus sync can replace or delete RFC-named files.

Mitigation: Use HTTPS lookups for routine work; if syncing the corpus, use a dedicated RFC directory.

Risk: The rsync mirror does not authenticate its source, and the prebuilt index relies on project GitHub releases.

Mitigation: Prefer HTTPS retrieval when source integrity matters.

## Reference(s):

- [RFC Editor RFC Index](https://www.rfc-editor.org/rfc-index.txt)
- [RFC Lookup 0.6.1 release changelog](https://github.com/shbernal/rfc-ai-tooling/releases/tag/v0.6.1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with section-scoped RFC excerpts and citations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Focused excerpts with RFC status and obsolescence information.]

## Skill Version(s):

0.6.1 (source: server-resolved release; scripts/rfc.py)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
