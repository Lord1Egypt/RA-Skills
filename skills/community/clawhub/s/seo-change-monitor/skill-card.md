## Description:

Catch SEO regressions after a deploy by snapshotting key URLs (status, redirects, canonical, robots, titles, schema, hreflang, robots.txt, sitemaps) and diffing against a saved baseline. Use for "did the release break SEO", "monitor SEO changes", "add an SEO check to CI" or before and after a launch.

This skill is ready for commercial/non-commercial use.

## Publisher:

[romeoseo](https://clawhub.ai/user/romeoseo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and SEO teams use this skill to compare a site's key SEO signals before and after a release, identify likely regressions, and prepare follow-up checks in Search Console. It can also provide a small CI script and release checklist.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review could not verify some local references because they were not present among the bundled artifacts.

Mitigation: Review any referenced project files or scripts in your own environment before installing.

## Reference(s):

- [ClawHub release](https://clawhub.ai/romeoseo/skills/seo-change-monitor)
- [SEO Change Monitor documentation](https://romeoseo.com/skills/seo-change-monitor)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown reports and checklists with JSON snapshots, Python code, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prioritized SEO changes, a Search Console watch list, and optional CI failure on Fix now findings]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
