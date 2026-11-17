## Description:

Sniplink saves user-submitted URLs for tools and services by extracting metadata, categorizing and tagging entries, and storing approved records as Obsidian notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[almohalhel1408](https://clawhub.ai/user/almohalhel1408)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Sniplink to quickly save, organize, and retrieve URLs for tools and services without filling out multi-step forms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes persistent notes to a hardcoded Google Drive-backed Obsidian path.

Mitigation: Configure a user-controlled storage location and require confirmation of the destination and final filename before saving.

Risk: The X/Twitter workflow can send tweet URLs to FxTwitter.

Mitigation: Use that path only when the user is comfortable sharing the tweet URL with the third-party service, or ask the user to paste tweet text instead.

Risk: Metadata collected from saved pages is untrusted and may be written into Markdown or YAML.

Mitigation: Review extracted metadata and sanitize filenames, Markdown, and YAML frontmatter before persisting notes.

## Reference(s):

- [Sniplink on ClawHub](https://clawhub.ai/almohalhel1408/skills/sniplink)
- [FxTwitter API endpoint used by the skill](https://api.fxtwitter.com/{user}/status/{id})

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown summaries and Obsidian note content with YAML frontmatter, plus inline shell commands when querying URLs or GitHub repositories.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user approval before saving; stored records may include source URLs, tags, categories, pricing notes, and social links.]

## Skill Version(s):

3.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
