## Description:

Generate SEO-optimized title, SEO title, SEO description, SEO slug, and social tips for a blog post, using current research and saving the result as JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dishant0406](https://clawhub.ai/user/dishant0406)

### License/Terms of Use:

MIT-0

## Use Case:

Writers, editors, and developers use this skill to generate researched SEO metadata for a single blog post stored under ~/blogs and save validated metadata under ~/blog-meta.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads blog drafts from ~/blogs and uses public research sites to shape metadata.

Mitigation: Review the selected blog file and researched sources before using the generated metadata for publication.

Risk: The skill saves generated metadata under ~/blog-meta and may overwrite an existing JSON file with the same SEO slug.

Mitigation: Check the target output path before accepting or rerunning the generated save operation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dishant0406/skills/re-blog-meta)
- [Meta Research](references/meta-research.md)
- [Meta Output](references/meta-output.md)
- [Human Voice](references/human-voice.md)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [JSON file plus a text completion report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes one metadata file to ~/blog-meta/<seo_slug>.json and reports the blog path, saved path, generated fields, research sources, and browser tab closure.]

## Skill Version(s):

1.1.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
