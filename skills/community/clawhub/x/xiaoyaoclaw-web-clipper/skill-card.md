## Description:

Saves user-selected web pages as local Markdown with YAML frontmatter, using article extraction with fallback and URL deduplication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dtsola](https://clawhub.ai/user/dtsola)

### License/Terms of Use:

MIT

## Use Case:

Developers and knowledge-work users use the skill to clip specific web pages into a local Markdown knowledge collection, with metadata and optional batch processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is incomplete: some local references were unresolved and the bundled QR image was outside static analyzer coverage.

Mitigation: Review unresolved references and the QR image before deciding whether to install.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dtsola/skills/xiaoyaoclaw-web-clipper)
- [Project documentation](https://github.com/dtsola/xiaoyaoclaw-web-clipper)

## Skill Output:

**Output Type(s):** [Files, Markdown]

**Output Format:** [Markdown files with YAML frontmatter]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single or batch URL clipping; local files include source metadata and are deduplicated by URL.]

## Skill Version(s):

1.0.18 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
