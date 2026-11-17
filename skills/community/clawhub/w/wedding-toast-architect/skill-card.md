## Description:

Helps wedding speakers plan a role-specific toast, review a draft for potentially awkward content, and estimate speaking time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

Wedding party members, family, friends, and speechwriters use this skill to outline, revise, and time wedding toasts. It helps identify potentially inappropriate references before the speech is delivered.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scanning a draft reads the local file supplied by the user.

Mitigation: Only pass draft paths you intend the tool to read.

Risk: Pattern matching may miss context or flag acceptable wording.

Mitigation: Review findings in context and read the final toast yourself before delivery.

## Reference(s):

- [Wedding Toast Architect on ClawHub](https://clawhub.ai/voronindenis5/skills/wedding-toast-architect)
- [Toast Craft](references/toast-craft.md)
- [Scanner Pattern Reference](references/scanner-patterns.md)

## Skill Output:

**Output Type(s):** [Markdown, Text, Guidance]

**Output Format:** [Text outlines, draft-review reports, and speaking-time estimates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Section word budgets; CUT, SOFTEN, and CHECK findings; delivery-time estimates]

## Skill Version(s):

1.0.1 (source: frontmatter, ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
