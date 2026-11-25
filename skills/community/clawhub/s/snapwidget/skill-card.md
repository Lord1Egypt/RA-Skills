## Description:

Add social media feeds (Instagram, Facebook, TikTok, X, YouTube) and reviews (Google, G2, testimonials) to a website with SnapWidget. Use when the user wants an Instagram feed, social posts, a YouTube channel, Google or G2 reviews or testimonials on their website, or wants to change or install a SnapWidget widget.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snapwidget](https://clawhub.ai/user/snapwidget)

### License/Terms of Use:

MIT-0

## Use Case:

Website owners and developers use this skill to connect their own or authorized social accounts and review sources, configure SnapWidget feeds or review widgets, and install them on a website.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Social account content or testimonial details may be shared with SnapWidget and displayed publicly.

Mitigation: Connect only sources the user owns or has permission to use; review testimonial details and public display before adding them.

Risk: Embedded widgets load externally hosted scripts on the website.

Mitigation: Review and approve the embed code and its external script before installing it on a live site.

Risk: Some platform instructions may weaken site protections to allow scripts or iframes.

Mitigation: Check those recommendations against the site's security needs and avoid weakening protections unless the user accepts the effect.

Risk: The security analysis was partial because a local path-like reference could not be resolved.

Mitigation: Review the relevant skill instructions and references before use; treat the scan results as incomplete.

## Reference(s):

- [SnapWidget documentation](https://snapwidget.com/docs)
- [Website builder installation guides](references/index.md)
- [JavaScript framework installation guide](references/frameworks.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration instructions, API calls]

**Output Format:** [Markdown guidance with CLI or MCP steps, code snippets, and website setup instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Platform-specific steps; account access, widget IDs, and embed code depend on the user's SnapWidget setup.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
