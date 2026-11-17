## Description:

A WeChat public-account writing assistant that helps with topic ideation, source and image research, article drafting, human-style polishing, Markdown formatting, and optional draft upload.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onceyoungs](https://clawhub.ai/user/onceyoungs)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, technical bloggers, and social media operators use this skill to plan, draft, polish, illustrate, and prepare WeChat public-account articles. It can also guide optional draft upload after the user reviews the generated title, summary, body, and image links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries for article research or image discovery may disclose sensitive draft topics or private terms to Tavily.

Mitigation: Avoid sending sensitive internal drafts, customer data, or private topics to Tavily unless sharing those terms with the service is intended.

Risk: The optional publish flow can create a WeChat draft using generated title, author, abstract, body, and image URLs.

Mitigation: Review all generated fields and image links before sending content to the WeChat publishing tool.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/onceyoungs/skills/wx-mp-write)
- [Publisher profile](https://clawhub.ai/user/onceyoungs)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, API Calls]

**Output Format:** [Markdown article drafts, source notes, image suggestions, and publishing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require TAVILY_API_KEY for search and a WeChat publishing tool for draft upload.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
