## Description:

Exports batches of Xiaohongshu (RedNote) note links into individual Markdown files and an index, including available note text, image OCR, video transcripts, and engagement details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackchew7143](https://clawhub.ai/user/jackchew7143)

### License/Terms of Use:

MIT-0

## Use Case:

Users who provide several Xiaohongshu note links can save the readable content as Markdown for archiving or later AI analysis. The export can include available OCR, transcripts, topics, engagement data, and comments, with a batch index.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted note links are sent to LinkDigest and returned text is written to local files; the security scan reports partial coverage.

Mitigation: Check that the links are appropriate to share, review the output directory, and treat the scan as incomplete.

## Reference(s):

- [LinkDigest Xiaohongshu export guide](https://linkdigest.dev/zh/xiaohongshu-biji-daochu?ref=skill-xiaohongshu-batch-export)

## Skill Output:

**Output Type(s):** [Files, Markdown, JSON]

**Output Format:** [Markdown note files and a Markdown batch index; single-note reads can also return JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One file per readable note plus an index; exports text rather than image or video files.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
