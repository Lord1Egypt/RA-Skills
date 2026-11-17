## Description:

Render structured data as beautiful hosted web pages, and create hosted forms for data collection, using the RenderKit API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antoinedc](https://clawhub.ai/user/antoinedc)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to create hosted visual pages for structured content and hosted forms for surveys, RSVPs, signups, feedback, and other data collection workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Rendered page content, form definitions, and respondent submissions are sent to RenderKit.

Mitigation: Avoid sending secrets, regulated personal data, or sensitive respondent data unless RenderKit privacy, retention, and compliance terms have been reviewed.

Risk: The form-close example uses DELETE and the artifact does not state whether closing a form is reversible.

Mitigation: Confirm intent and preserve needed responses before using the close-form command.

## Reference(s):

- [RenderKit Homepage](https://renderkit.live)
- [RenderKit API Docs](https://renderkit.live/docs.md)
- [ClawHub Skill Page](https://clawhub.ai/antoinedc/skills/renderkit)
- [Publisher Profile](https://clawhub.ai/user/antoinedc)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with curl command examples and API usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires RENDERKIT_API_KEY and curl; generated pages, forms, and form responses are hosted by RenderKit.]

## Skill Version(s):

1.4.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
