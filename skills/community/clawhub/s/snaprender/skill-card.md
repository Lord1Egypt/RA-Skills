## Description:

Screenshot any web page as an image (desktop or phone, cookie pop-ups blocked) or read it as markdown, with the SnapRender API. Use when the user wants to see, capture, compare or check how a website looks, or read a page.

This skill is ready for commercial/non-commercial use.

## Publisher:

[user0856](https://clawhub.ai/user/user0856)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can ask an agent to capture a website as an image, read page content as Markdown or text, or monitor a page for changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Target URLs and accessible page contents are sent to SnapRender for capture or extraction.

Mitigation: Use the skill only with pages the user authorizes and avoid sending sensitive page content.

Risk: The skill can create recurring page-monitoring schedules and check account usage.

Mitigation: Create schedules only when requested, and review active schedules and account activity.

Risk: Scanner coverage is incomplete because a local path-like reference could not be resolved.

Mitigation: Review the skill contents before installation and use.

## Reference(s):

- [SnapRender agent guide](https://snap-render.com/ai-agents)
- [SnapRender documentation](https://snap-render.com/docs)
- [ClawHub skill listing](https://clawhub.ai/user0856/skills/snaprender)

## Skill Output:

**Output Type(s):** [Images, Markdown, Text]

**Output Format:** [Screenshot image files (JPEG, PNG, WebP, or PDF) and extracted page content as Markdown or text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Capture and extraction options vary by request; page monitoring can create scheduled captures.]

## Skill Version(s):

1.6.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
