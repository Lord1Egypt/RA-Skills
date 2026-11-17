## Description:

Transform document photos into clean scanned-looking pages with automatic edge detection, cropping, and perspective correction. Use when (1) the user wants a photo to look scanned; (2) receipts, forms, pages, or papers need clean borders and straightening; (3) the result should be easier to read, share, archive, or pass to OCR.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to turn document photos, receipts, forms, and sheets into cleaner scan-style outputs with edge detection, cropping, and perspective correction guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned npm tooling and mutable CDN scripts can change between runs.

Mitigation: Use pinned package versions, lockfile-managed installs, immutable script URLs, or vendored reviewed copies before deployment.

Risk: Browser-loaded third-party scripts may process sensitive document images.

Mitigation: Avoid using pages with mutable third-party scripts for identity, financial, legal, medical, or business documents.

Risk: Automatic edge detection can select incorrect corners on poor inputs.

Mitigation: Review the output visually and retry with a cleaner image or manual-corner flow when detection is wrong.

## Reference(s):

- [OpenCV.js 4.7.0](https://docs.opencv.org/4.7.0/opencv.js)
- [OpenCV Documentation](https://docs.opencv.org/)
- [jscanify CDN Source](https://cdn.jsdelivr.net/gh/ColonelParrot/jscanify@master/src/jscanify.min.js)
- [Scanner Skill Page](https://clawhub.ai/ivangdavila/skills/scanner)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell, HTML, and JavaScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Browser-first document scanning workflow using jscanify; recommends visual review before accepting crops.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
