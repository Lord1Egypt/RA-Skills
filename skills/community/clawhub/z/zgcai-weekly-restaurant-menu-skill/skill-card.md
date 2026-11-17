## Description:

Extracts structured weekly menu content, including breakfast, lunch, and snacks by day, from a cafeteria or canteen menu image using a vision-language model through OpenRouter.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ihainan](https://clawhub.ai/user/ihainan)

### License/Terms of Use:

MIT-0

## Use Case:

Agents supporting cafeteria users use this skill to convert a weekly menu photo into structured Markdown with the week date range and dish lists for each day. It is useful when users need to quickly reference breakfast, lunch, and snack stall options from PNG or JPEG menu images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script can send any readable local file path to OpenRouter without validating that the file is a menu image.

Mitigation: Only pass trusted PNG or JPEG menu images from an upload or workspace directory, avoid images containing private information, and prefer a release that validates image type, size, and allowed paths.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ihainan/skills/zgcai-weekly-restaurant-menu-skill)
- [OpenRouter chat completions endpoint](https://openrouter.ai/api/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Structured Markdown menu extraction with command-line status details on stderr]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MENU_OPENROUTER_API_KEY and sends the selected image file to OpenRouter.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
