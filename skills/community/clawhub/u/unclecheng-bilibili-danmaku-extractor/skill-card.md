## Description:

Extracts public Bilibili video danmaku from a BV ID or video URL and exports the results as JSON and Markdown files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unclecheng-li](https://clawhub.ai/user/unclecheng-li)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to fetch publicly available danmaku for a Bilibili video and save time-ordered exports for analysis, archiving, or review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts Bilibili public APIs and writes extracted public comments to a selected output directory.

Mitigation: Run it only where outbound Bilibili access and local file output are acceptable, and choose an output directory intended for extracted data.

Risk: Generated Markdown contains third-party danmaku text that may be unsafe to render or pass into another AI system without review.

Mitigation: Treat exported Markdown as untrusted content; inspect or sanitize it before permissive rendering or downstream AI use.

Risk: The dependency specification allows future requests versions, which can reduce install reproducibility.

Mitigation: Pin dependencies in deployment environments when reproducible installs are required.

Risk: Bilibili may rate-limit or reject requests, resulting in 403 or 412 responses.

Mitigation: Control request frequency and retry later if public API access is temporarily blocked.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unclecheng-li/skills/unclecheng-bilibili-danmaku-extractor)
- [ClawHub publisher profile](https://clawhub.ai/user/unclecheng-li)
- [Bilibili video info API](https://api.bilibili.com/x/web-interface/view?bvid={bvid})
- [Bilibili danmaku API](https://api.bilibili.com/x/v1/dm/list.so?oid={cid})

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with Python and shell examples; generated JSON and Markdown export files when the script is run.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3.8+, network access to Bilibili public APIs, and the requests package.]

## Skill Version(s):

1.0.0 (source: server release metadata and _skillhub_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
