## Description:

Generates modern SaaS product landing pages in multiple styles and outputs deployable HTML, CSS, React, Vue, or Next.js code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunshine-del-ux](https://clawhub.ai/user/sunshine-del-ux)

### License/Terms of Use:

MIT

## Use Case:

Developers, founders, and marketing teams use this skill to scaffold responsive SaaS landing pages with common marketing sections, SEO metadata, and deployable frontend code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script can write outside the intended folder when product names or output paths are uncontrolled.

Mitigation: Choose an output directory deliberately, avoid sensitive project roots, block path traversal, slugify product names, and refuse accidental overwrites.

Risk: Untrusted product names or descriptions can be inserted into deployable HTML or JSX.

Mitigation: Use only trusted product text, escape generated HTML/JSX content, and inspect generated files before opening or deploying them.

Risk: Generated pages may depend on frontend assets loaded from public CDNs.

Mitigation: Pin dependency versions or bundle frontend dependencies before production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sunshine-del-ux/skills/saas-landing-page-generator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Generated project files with Markdown usage guidance and optional shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can generate HTML, React, Vue, or Next.js landing-page projects with Tailwind, Bootstrap, or plain CSS styling options.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
