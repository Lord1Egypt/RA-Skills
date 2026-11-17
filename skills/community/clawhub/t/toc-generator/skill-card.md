## Description:

Helps agents add, optimize, or audit table-of-contents structures for long-form content, including jump links, heading structure, semantic HTML, SEO, UX, mobile, and accessibility guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kostja94](https://clawhub.ai/user/kostja94)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and content teams use this skill when they want an agent to plan or audit table-of-contents patterns for long-form articles, guides, whitepapers, or documentation. It focuses on practical TOC structure, heading and anchor ID mapping, HTML/ARIA notes, SEO checks, and responsive UX considerations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate for nearby content-structure requests such as article navigation or content outlines.

Mitigation: Confirm that the user wants TOC or in-page navigation guidance before applying TOC-specific recommendations.

Risk: The skill may read local project context files when present to understand content structure.

Mitigation: Review local project context files for sensitive information before using them as grounding for public-facing TOC guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kostja94/skills/toc-generator)
- [Publisher profile](https://clawhub.ai/user/kostja94)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown with HTML snippets, checklists, and structured recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include TOC nesting, heading/ID mapping suggestions, HTML/ARIA notes, SEO checklist items, and mobile/accessibility guidance.]

## Skill Version(s):

1.0.1 (source: server evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
