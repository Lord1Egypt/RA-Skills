## Description:

Writes YouTube packaging for a video - title options, description with chapters and links, tags, category, made-for-kids declaration and a thumbnail brief - into metadata.json and validates it against YouTube limits. Use when the user needs a YouTube title, description, tags, chapters or thumbnail idea.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahmadhussain0335](https://clawhub.ai/user/ahmadhussain0335)

### License/Terms of Use:

MIT

## Use Case:

Creators and their assistants use this skill to prepare YouTube video metadata from a script, including title options, a description, tags, category and made-for-kids declaration, plus a thumbnail brief. It writes and checks metadata.json against YouTube limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated metadata may have an incorrect language, category or made-for-kids declaration.

Mitigation: Review the generated metadata and confirm these fields before publishing.

Risk: The required socialkit-social-core companion skill was not included in the inspected bundle.

Mitigation: Review socialkit-social-core separately before applying its guidance.

## Reference(s):

- [Common YouTube category IDs](references/categories.md)
- [YouTube Data API quota costs](https://developers.google.com/youtube/v3/determine_quota_cost)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON configuration]

**Output Format:** [metadata.json plus a Markdown thumbnail brief in the reply]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Offers 3–5 title options and up to 15 tags; requires the user to choose a category and explicitly declare made-for-kids status.]

## Skill Version(s):

0.3.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
