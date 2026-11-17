## Description:

Capture a full-page PNG screenshot of a public URL through Scavio and return it as an inline base64 data:image/png URI with capture mode and image size metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to capture full-page website screenshots for previews, reports, slide decks, PDFs, OCR or vision-model inputs, visual diffing, and archiving current page state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requested URLs are sent to Scavio as a third-party screenshot service.

Mitigation: Use the skill only for URLs that are appropriate to disclose to Scavio and avoid private or sensitive targets.

Risk: SCAVIO_API_KEY is required and grants access to the screenshot API account.

Mitigation: Store the key in an environment variable or secret store, avoid committing it to source control, and rotate it if exposed.

Risk: Successful captures consume credits, and ultra mode costs more than normal or advanced mode.

Mitigation: Start with normal mode, escalate only when screenshots are blank or incomplete, and monitor remaining credits.

Risk: Inline base64 screenshot data can be large.

Mitigation: Decode the data URI to a PNG file for downstream use instead of pasting large base64 strings into prompts or documents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/scavio-ai/skills/website-screenshot-api)
- [Scavio documentation](https://scavio.dev/docs?utm_source=agent-skills&utm_medium=skill&utm_campaign=website-screenshot-api)
- [Scavio signup](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=website-screenshot-api)
- [Scavio rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=website-screenshot-api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON, Python, and curl examples; runtime API response is JSON containing a base64 PNG data URI.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SCAVIO_API_KEY. Screenshots are always full-page PNG images returned inline as data:image/png;base64 URIs. Normal and advanced modes cost 1 credit; ultra mode costs 5 credits; only successful captures are billed.]

## Skill Version(s):

1.0.3 (source: server release evidence; artifact frontmatter declares 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
