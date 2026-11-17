## Description:

Finds valid WebCodecs strings for video and audio by researching codec support tables and detailed specifications on webcodecsfundamentals.org.

This skill is ready for commercial/non-commercial use.

## Publisher:

[socratescli](https://clawhub.ai/user/socratescli)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to select WebCodecs video or audio codec strings for target browsers, platforms, codecs, and media requirements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recommendations depend on external WebCodecs support data that may change over time.

Mitigation: Verify recommendations against current WebCodecs Fundamentals pages and target browser or platform support before relying on them.

Risk: Unpinned third-party skill updates could differ from the reviewed release.

Mitigation: Before installing or upgrading, prefer a pinned commit or reviewed release and re-check the repository.

## Reference(s):

- [WebCodecs Fundamentals codec support table](https://webcodecsfundamentals.org/datasets/codec-support-table/)
- [WebCodecs Fundamentals codec detail pages](https://webcodecsfundamentals.org/codecs/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown recommendation list with brief explanations and browser or platform support notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Usually returns 2-3 codec string recommendations.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
