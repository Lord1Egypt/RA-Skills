## Description:

RenderingVideo preview assistant that uses the public preview flow at POST /api/preview without an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gljhint](https://clawhub.ai/user/gljhint)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to draft or edit RenderingVideo schema JSON, validate it through the public preview endpoint, and return a temporary preview URL and identifier.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: RenderingVideo schema JSON is sent to a public preview service.

Mitigation: Use only schemas that are acceptable to send externally; avoid secrets, private internal URLs, proprietary unreleased content, and personal data unless that exposure is acceptable.

Risk: Preview links are temporary and shareable.

Mitigation: Treat returned preview links as externally shareable and regenerate previews when links expire or become invalid.

Risk: Schema or API validation failures can prevent preview generation.

Mitigation: Validate JSON locally, follow RenderingVideo documentation for supported fields, and preserve API error details for troubleshooting.

## Reference(s):

- [RenderingVideo API and usage documentation](https://renderingvideo.com/docs/api-and-usage.md)
- [RenderingVideo JSON specification](https://renderingvideo.com/docs/json-spec.md)
- [RenderingVideo clips documentation](https://renderingvideo.com/docs/clips.md)
- [RenderingVideo elements documentation](https://renderingvideo.com/docs/elements.md)
- [RenderingVideo base clip documentation](https://renderingvideo.com/docs/elements/base-clip.md)
- [RenderingVideo animation and timing documentation](https://renderingvideo.com/docs/animation-and-timing.md)
- [RenderingVideo public preview endpoint](https://video.renderingvideo.com/api/preview)
- [ClawHub skill page](https://clawhub.ai/gljhint/skills/renderingvideo-generator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with JSON schema edits, shell command results, preview URLs, and temporary preview identifiers.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preview links are temporary and shareable; the selected RenderingVideo schema JSON is sent to a public preview service.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
