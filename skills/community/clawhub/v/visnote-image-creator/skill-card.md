## Description:

This skill helps agents generate XiaoHongShu-style social media images by selecting VisNote templates, preparing template data, and invoking the image generation script.

This skill is ready for commercial/non-commercial use.

## Publisher:

[katherine0325](https://clawhub.ai/user/katherine0325)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers use this skill to produce VisNote-based XiaoHongShu covers, content images, comparison images, and tutorial visuals from natural-language requirements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a real VisNote API key and may expose it if configuration files or generated command context are shared carelessly.

Mitigation: Keep config.json out of version control, avoid sharing logs or screenshots that reveal credentials, and rotate any key that may have been exposed.

Risk: The generation script accepts an optional server override, which can send requests and credentials to a non-official endpoint.

Mitigation: Use only the official VisNote server and avoid passing --server unless the endpoint is explicitly trusted.

Risk: Browser automation dependencies can change behavior across releases.

Mitigation: Use pinned Playwright dependencies and re-test image generation after dependency updates.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/katherine0325/skills/visnote-image-creator)
- [VisNote homepage](https://vis-note.netlify.app)
- [VisNote profile and API key page](https://vis-note.netlify.app/profile)
- [VisNote template API](https://vis-note.netlify.app/api/open/templates)
- [README](artifact/README.md)
- [Skill instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Files]

**Output Format:** [Markdown guidance with shell commands and JSON configuration examples; the invoked script writes image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a VisNote API key in config.json, Node.js, Playwright Chromium, and access to the VisNote service.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
