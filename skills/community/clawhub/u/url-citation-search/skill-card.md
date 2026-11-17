## Description:

Find papers and preprints that cite a given URL, especially blogs, docs pages, project pages, or other web content that standard citation indexes often miss.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zjsxply](https://clawhub.ai/user/zjsxply)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, developers, and analysts use this skill to find and verify academic papers or preprints that cite a supplied web URL. It is especially useful for web pages, documentation, project pages, and other non-paper sources that standard citation indexes may miss.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs web and academic-source research on user-provided URLs, so results can be incomplete when search indexes, PDFs, or publisher metadata omit citations.

Mitigation: Verify candidate citing works against PDF text, HTML references, metadata, or link annotations before reporting them as confirmed citations.

Risk: A paper on the same topic may appear relevant without actually citing the target URL.

Mitigation: Reject matches unless the target URL, title, slug, or verified mirror appears in the citing work's reference evidence.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zjsxply/skills/url-citation-search)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown citation report, brief list, or BibTeX when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May distinguish confirmed citations from candidates and direct, official variant, or mirror citations.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
