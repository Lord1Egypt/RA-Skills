## Description:

Formats existing draft text into a Xiaohongshu-style note with title ideas, paragraphing, hashtag suggestions, word count, and a pre-publish checklist.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangshengli0421](https://clawhub.ai/user/wangshengli0421)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and social media operators use this skill to structure existing Xiaohongshu draft text or bullet points into Markdown with candidate titles, body sections, topic tags, and a pre-publish checklist. It supports formatting and structure, not full deep creative copywriting on its own.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A user-provided draft file path is read locally for formatting.

Mitigation: Use this skill with non-sensitive social post drafts and review the selected file path before execution.

Risk: The generated hashtag suggestions and compliance checklist are rule-based drafting aids and may be incomplete for regulated content.

Mitigation: Review tags, claims, and checklist items before publishing, especially for medical, financial, or advertising-sensitive topics.

## Reference(s):


## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown generated from local text input]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads UTF-8 draft text from --file or --text and applies a configurable max-body limit, defaulting to 900 characters.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
