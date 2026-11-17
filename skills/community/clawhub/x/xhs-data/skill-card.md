## Description:

Collects public Xiaohongshu note, user, search, comment, and media data using API and browser automation engines.

This skill is for research and development only.

## Publisher:

[cooperiano](https://clawhub.ai/user/cooperiano)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data practitioners use this skill to guide Xiaohongshu public-content collection workflows, including note extraction, user homepage crawling, keyword search, comment retrieval, and media downloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using login or session data may create account and platform-policy risk.

Mitigation: Only provide Xiaohongshu login or session data after reviewing account, consent, and platform implications.

Risk: Collected content and media may persist locally under fixed output paths.

Mitigation: Review the configured output directories before and after runs and remove retained data that is no longer needed.

Risk: Unpinned Python dependencies can change behavior or introduce supply-chain exposure.

Mitigation: Install dependencies in an isolated virtual environment and review or pin package versions before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cooperiano/skills/xhs-data)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe JSON, Markdown, HTML, media files, and local directory outputs created by downstream scraping scripts.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
