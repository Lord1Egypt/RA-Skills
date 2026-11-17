## Description:

Deprecated SciVerse skill for academic-paper metadata search, semantic chunk retrieval, and byte-range content reading; new installations should migrate to academic-retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sciverse](https://clawhub.ai/user/sciverse)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill to find academic papers, retrieve citation-oriented semantic excerpts, and expand retrieved chunks with original text ranges. Because the release is deprecated, new workflows should prefer academic-retrieval when available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Custom endpoint settings may expose the SciVerse API token, research queries, and requested document identifiers over unencrypted HTTP.

Mitigation: Keep SCIVERSE_BASE_URL unset or set it only to a trusted HTTPS SciVerse endpoint.

Risk: This deprecated slug will not receive new features or fixes.

Mitigation: Prefer the renamed academic-retrieval skill when available.

## Reference(s):

- [SciVerse Homepage](https://sciverse.space)
- [Academic Retrieval Replacement Skill](https://clawhub.ai/academic-retrieval)
- [ClawHub Skill Page](https://clawhub.ai/sciverse/skills/sciverse-agent-tools)

## Skill Output:

**Output Type(s):** [json, text, guidance]

**Output Format:** [JSON API responses and text fragments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SCIVERSE_API_TOKEN; optional SCIVERSE_BASE_URL should remain unset unless a trusted SciVerse HTTPS endpoint is required.]

## Skill Version(s):

0.1.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
