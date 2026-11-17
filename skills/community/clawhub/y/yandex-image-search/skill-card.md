## Description:

Reverse image search for finding image sources, visually similar images, and authenticity context using Yandex, Google Lens, and Bing with URL or local file inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnsonsleo](https://clawhub.ai/user/johnsonsleo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill when a user supplies an image URL or local file and asks to identify its origin, find visually similar images, or assess surrounding authenticity context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local file inputs can upload any readable path to third-party search providers.

Mitigation: Use only image files intentionally selected for reverse search, require confirmation for local uploads, and constrain allowed paths before use.

Risk: Yandex diagnostics can write debug HTML files to /tmp when failures occur.

Mitigation: Avoid using sensitive images, review debug output before sharing logs, and remove temporary debug files after troubleshooting.

Risk: Search results depend on third-party services that may return anti-bot responses or break when upstream pages change.

Mitigation: Treat non-zero exits and error JSON as retry or fallback signals, and manually verify important matches before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/johnsonsleo/skills/yandex-image-search)
- [Yandex image search base URL](https://yandex.com)
- [Yandex regional image search base URL](https://yandex.ru)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [JSON search results with optional Markdown summary guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts an image URL or local file path, optional search engine, and optional result limit; no API key is required.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
