## Description:

SeaPortal helps agents fetch static or server-rendered web pages as clean Markdown, JSON accessibility snapshots, TEI XML, sitemaps, feeds, and site digests without running a browser.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pinchtab](https://clawhub.ai/user/pinchtab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use SeaPortal to read, navigate, and summarize static or server-rendered websites quickly without launching a full browser. It is useful for page extraction, accessibility snapshot inspection, sitemap and feed parsing, and deciding when a browser-based tool is required.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and runs a mutable third-party executable.

Mitigation: Review the dependency source before installing and prefer pinned or otherwise verified releases.

Risk: Proxy examples may encourage placing credentials directly in command-line URLs.

Mitigation: Avoid real proxy passwords in command-line arguments when possible and use credential handling appropriate for the host environment.

Risk: Cached, saved, or split fetch outputs may contain sensitive or copyrighted page content.

Mitigation: Clean up cache and output directories after use and limit filesystem access to locations needed for the task.

Risk: HTTP-only extraction does not execute JavaScript or support stateful browser interactions.

Mitigation: Use SeaPortal for static or server-rendered pages and escalate to a real browser when pages are SPA-only, blocked, authenticated, or require forms or clicks.

## Reference(s):

- [ClawHub SeaPortal skill page](https://clawhub.ai/pinchtab/skills/seaportal)
- [SeaPortal homepage](https://github.com/pinchtab/seaportal)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples; SeaPortal commands can emit Markdown, JSON, XML, compact text, TSV manifests, or files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports token caps, chunking, link and media extraction, optional cache directories, and optional saved or split output files.]

## Skill Version(s):

0.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
