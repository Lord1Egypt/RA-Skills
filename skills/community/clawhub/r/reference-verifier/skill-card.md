## Description:

Automatically checks academic references in AI-generated content, validates citation authenticity across academic databases, assesses topical relevance, generates corrected BibTeX and APA citations, recommends replacement sources, and supports PDF citation matching.

This skill is ready for commercial/non-commercial use.

## Publisher:

[793943403](https://clawhub.ai/user/793943403)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, students, and research-writing teams use this skill to verify bibliography entries, identify hallucinated or questionable citations, repair citation formats, and compare PDF body citations with reference lists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploaded manuscripts or citation lists may expose confidential, unpublished, or proprietary research details during external academic database verification.

Mitigation: Use only material suitable for external metadata checks, or remove sensitive content before requesting verification.

Risk: Academic database lookups can fail, disagree, or miss valid references, leading to uncertain citation classifications.

Mitigation: Treat questionable or hallucinated labels as review prompts and manually confirm important citations against primary publisher records or DOI resolvers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/793943403/skills/reference-verifier)
- [Publisher profile](https://clawhub.ai/user/793943403)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, Guidance]

**Output Format:** [Markdown reports with tables, citation-status labels, BibTeX and APA citation text, replacement-source recommendations, and PDF matching summaries when provided.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May rely on external academic database verification and should avoid confidential, unpublished, or proprietary manuscripts unless that processing is acceptable.]

## Skill Version(s):

1.3.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
