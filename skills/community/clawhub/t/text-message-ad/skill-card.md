## Description:

Creates animated iMessage-style conversation ads as self-contained HTML and 1080x1920 MP4s with synthesized message sounds for marketing and product demos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oasiseng](https://clawhub.ai/user/oasiseng)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams, founders, and creative operators use this skill to turn product details, logos, pain points, and proof points into short vertical chat-style ads. The skill is intended for fictional, disclosed dramatizations rather than real conversations or testimonials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-supplied ad text, domains, logos, or brand files may be inserted into raw HTML and become executable content in rendered or delivered files.

Mitigation: HTML-escape all inserted text, validate URLs, colors, and images, add a restrictive CSP, and block external browser requests during rendering.

Risk: Generated chat-style ads could be mistaken for real conversations or testimonials.

Mitigation: Use only fictional characters, avoid real-person impersonation or fake testimonials, and add a visible dramatization disclosure when required by a platform or reviewer.

Risk: Rendering may create multiple generated files from user-provided inputs.

Mitigation: Keep generated HTML, frames, audio, and video outputs in a dedicated output directory and review the final HTML and MP4 before delivery.

## Reference(s):

- [Brand Checklist & Design Patterns](references/brand-checklist.md)
- [ClawHub skill page](https://clawhub.ai/oasiseng/skills/text-message-ad)
- [Publisher profile](https://clawhub.ai/user/oasiseng)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with HTML, JSON configuration, shell commands, and generated media files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces self-contained animated HTML, rendered PNG frames, synthesized WAV audio, a 1080x1920 MP4, and optional social captions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
