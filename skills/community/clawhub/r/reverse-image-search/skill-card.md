## Description:

Reverse Image Search helps agents use Yandex, Google, and Bing to find an image's source, visually similar images, or authenticity context from a URL or local file without an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gushu333](https://clawhub.ai/user/gushu333)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill when an agent needs to investigate an image's origin, similar web matches, or authenticity context from a user-provided image URL or local file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local images or image URLs may be sent to external reverse image search providers.

Mitigation: Use only images that may be shared with Yandex, Google, or Bing; avoid confidential, internal, or metadata-sensitive images unless consent and metadata handling have been addressed.

Risk: The setup installs PicImageSearch without a pinned version, so dependency behavior can change over time.

Mitigation: Pin and review PicImageSearch and its transitive dependencies before deployment in stricter environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gushu333/skills/reverse-image-search)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [JSON search results with optional Markdown summary guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include title, URL, thumbnail, source engine, and similarity when available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
