## Description:

Create shareable quote and reflection posters from books, films, documentaries, anime, or dramas using Mew image and design APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shuminliu026](https://clawhub.ai/user/shuminliu026)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to turn a book or film title, quote, takeaway, mood, and optional reference image into a polished social check-in poster. It guides input collection, Mew API use, output inspection, and final Markdown image-link delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Poster text, image URLs, optional watermark text, and the Mew API key are sent to Mew's external API.

Mitigation: Avoid sensitive personal content and use only API keys and image URLs the user is comfortable sharing with Mew.

Risk: Local or attached images are not directly usable by the downstream APIs and may require temporary upload to an external host.

Mitigation: Prefer user-provided public image URLs; request explicit consent before any temporary third-party upload.

Risk: Generated posters may be unreadable, visually generic, or have overlapping text.

Mitigation: Inspect the background and final poster, then retry once with stronger readability, negative-space, and typography cues when needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/shuminliu026/skills/quote-check-in-poster)
- [Publisher Profile](https://clawhub.ai/user/shuminliu026)
- [Mew API Key Setup](https://mew.design/login)
- [Mew Image Process API Endpoint](https://api.mew.design/open/api/image/process)
- [Mew Design Generate API Endpoint](https://api.mew.design/open/api/design/generate)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown image link and short explanatory text, with optional curl examples for Mew API calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns the final poster URL and a short mood summary after inspecting generated background and poster readability.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
