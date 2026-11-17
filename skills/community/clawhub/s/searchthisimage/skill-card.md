## Description:

Finds where an image appears online, visually similar images, and likely content using SearchThisImage with image URLs or uploaded files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[selvatuple](https://clawhub.ai/user/selvatuple)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to perform reverse image searches from an image URL or uploaded image file and present concise, readable results. It is useful when a user wants to identify image origins, matching pages, visually similar images, or related entities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Images or image URLs are sent to SearchThisImage for processing.

Mitigation: Use the skill only for images that are appropriate to share with SearchThisImage, and avoid private, confidential, or regulated images unless approved.

Risk: Command examples could mishandle crafted user input and run local commands.

Mitigation: Serialize JSON safely, validate HTTPS image URLs, create trusted temporary files, and avoid constructing shell commands directly from raw user input.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/selvatuple/skills/searchthisimage)
- [SearchThisImage API base URL](https://api.searchthisimage.com)
- [SearchThisImage privacy policy](https://searchthisimage.com/privacy.html)

## Skill Output:

**Output Type(s):** [markdown, API calls, shell commands, guidance]

**Output Format:** [Markdown response with links and concise result sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses curl with SEARCHTHISIMAGE_API_KEY and returns up to five matching pages, up to three visually similar image URLs, and related entities when available.]

## Skill Version(s):

1.0.4 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
