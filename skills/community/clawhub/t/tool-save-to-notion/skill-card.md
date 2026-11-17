## Description:

Saves tool URLs to a Notion Toolbox database by extracting the tool name, type, tags, description, and optional cover image.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redisread](https://clawhub.ai/user/redisread)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to save GitHub repositories, product pages, browser extensions, software packages, and online tools into a structured Notion Toolbox database. It helps collect the original URL, classification, tags, short description, and optional cover image for later discovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch user-supplied URLs, including private links, internal URLs, or sensitive repositories.

Mitigation: Require explicit confirmation before fetching a URL and avoid processing internal or sensitive links unless the user confirms the destination and data handling.

Risk: The skill creates persistent Notion records that may store sensitive links, extracted metadata, or page descriptions.

Mitigation: Use a tightly scoped Notion integration token and confirm that the target database is appropriate for the information being saved.

Risk: Untrusted page text can affect generated request payloads if it is inserted into curl JSON without safe serialization.

Mitigation: Generate JSON payloads with a safe serializer and review extracted fields before creating the Notion page.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/redisread/skills/tool-save-to-notion)
- [Publisher profile](https://clawhub.ai/user/redisread)
- [Notion integrations](https://www.notion.so/my-integrations)
- [Notion pages API endpoint](https://api.notion.com/v1/pages)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash/Python command examples and JSON API payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a NOTION_API_KEY environment variable and a Notion database shared with the integration.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
