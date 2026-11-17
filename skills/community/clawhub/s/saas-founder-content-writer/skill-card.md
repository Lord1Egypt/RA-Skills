## Description:

Use this skill when a creator, SaaS founder, indie hacker, or product builder wants to turn raw material such as product updates, user pain points, technical lessons, launches, or knowledge topics into high-signal posts for X, Reddit, LinkedIn, Xiaohongshu, or YouTube.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archlab-space](https://clawhub.ai/user/archlab-space)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, SaaS founders, indie hackers, and product builders use this skill to convert provided product or knowledge material into platform-specific social drafts, image briefs, and optional text/data graphics. It helps produce useful founder content while avoiding generic marketing copy, invented metrics, and unsupported claims.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The image renderer can open HTML in a browser with network access.

Mitigation: Review the renderer before use, render only trusted self-contained HTML, and consider request blocking or disabling JavaScript during rendering.

Risk: The renderer depends on the Puppeteer dependency chain.

Mitigation: Audit and update the Puppeteer dependencies before running npm install or using the renderer in a trusted environment.

Risk: Optional vault saving writes generated drafts and rendered images to a resolved local path.

Mitigation: Verify the resolved vault path before enabling save-to-vault auto-saving, and keep saving opt-in.

Risk: Generated founder content can include misleading claims if unsupported source material is treated as fact.

Mitigation: Use only founder-provided facts, metrics, quotes, and results; flag unsupported performance, security, financial, or compliance claims before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/archlab-space/skills/saas-founder-content-writer)
- [README](artifact/README.md)
- [Render Image Setup](artifact/render-image-setup.md)
- [Feedback and contributions](https://github.com/archlab-space/open-skill-hub/issues)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Files, Guidance]

**Output Format:** [Markdown draft blocks with platform-specific fields, optional image briefs, HTML/CSS snippets, render commands, and optional PNG files from the renderer.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can optionally save finalized drafts and rendered images to a user-approved vault folder; image rendering uses self-contained HTML/CSS and headless Chrome.]

## Skill Version(s):

0.12.0 (source: server release evidence and CHANGELOG, released 2026-06-15)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
