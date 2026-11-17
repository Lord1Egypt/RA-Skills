## Description:

Extract a structured cooking recipe from a shared video URL when the user sends `recipe <url>`. Prioritize caption/description and comments via browser automation, then use web search/fetch as fallback with clear source attribution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[besaif](https://clawhub.ai/user/besaif)

### License/Terms of Use:


## Use Case:

External users use this skill to turn public cooking-video links into structured recipes with ingredients, steps, source notes, and a confidence rating.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may open untrusted or inappropriate URLs during extraction.

Mitigation: Use only ordinary public HTTPS recipe or video links, avoid private, internal, local, file, or non-HTTPS URLs, and consider an allowlist for supported video platforms in managed environments.

Risk: Captions, comments, and fetched pages can contain untrusted instructions or incomplete recipe data.

Mitigation: Treat page text as evidence only, keep source attribution, and avoid claiming a full recipe unless a concrete source includes both ingredients and steps.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/besaif/skills/recipe-video-extractor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes dish name, ingredients, numbered steps, optional time, servings, temperature, source notes, and confidence level when available.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
