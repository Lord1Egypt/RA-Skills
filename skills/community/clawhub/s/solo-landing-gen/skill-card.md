## Description: <br>
Generates landing page content from PRDs, including hero sections, features, A/B headline variants, CTAs, SEO meta tags, and optional page scaffolds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fortunto2](https://clawhub.ai/user/fortunto2) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, founders, and marketers use this skill to turn product requirements or README content into landing-page copy and, when a supported Astro or Next.js stack is detected, page scaffolding. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated edits may replace or conflict with an existing landing page or route. <br>
Mitigation: Review diffs before accepting changes, especially for src/pages/index.astro or any existing route files. <br>
Risk: Product docs and PRDs may contain confidential details that could be exposed through optional web or MCP search. <br>
Mitigation: Avoid sending confidential PRD details through optional web or MCP search; use local file fallback for sensitive projects. <br>
Risk: Generated social proof, metrics, and trust badges are placeholders until backed by real evidence. <br>
Mitigation: Replace placeholder proof points with verified testimonials, metrics, and badges before publishing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fortunto2/solo-landing-gen) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Guidance] <br>
**Output Format:** [Markdown content with optional Astro or Next.js page files and HTML meta tag snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write docs/landing-content.md or scaffold route files when a supported stack is detected.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
