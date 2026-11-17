## Description:

UI Master helps agents build, refine, and review production-grade React and Next.js interfaces with Tailwind CSS v4 and shadcn/ui.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anjasta-tarigan](https://clawhub.ai/user/anjasta-tarigan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create polished product interfaces, set up Tailwind CSS v4 and shadcn/ui, establish design tokens, compose common application layouts, and audit UI quality. It is aimed at React and Next.js projects that need production-ready frontend guidance and code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup examples use mutable third-party package commands such as latest-version CLIs.

Mitigation: Pin CLI and package versions where possible, run setup from an unprivileged clean branch or disposable workspace, and review generated or overwritten files before committing.

Risk: UI scaffolding and component examples may need project-specific adaptation before production use.

Mitigation: Adapt examples to the target framework and existing design system, then verify accessibility, responsive behavior, loading states, error states, and reduced-motion behavior.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/anjasta-tarigan/skills/ui-master)
- [Publisher Profile](https://clawhub.ai/user/anjasta-tarigan)
- [Accessibility & Performance Checklist](references/accessibility-performance-checklist.md)
- [Design Tokens for Production UI](references/design-tokens.md)
- [Modern Effects Catalogue](references/modern-effects.md)
- [shadcn/ui Setup and Theming](references/shadcn-setup.md)
- [Tailwind CSS v4 Setup](references/tailwind-v4-setup.md)
- [shadcn/ui Schema](https://ui.shadcn.com/schema.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline code blocks and TypeScript/React examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be adapted to the user's project stack and verified for accessibility, responsiveness, and runtime behavior.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
