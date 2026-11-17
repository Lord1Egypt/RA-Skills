## Description:

Tailwind CSS v4 guidance for CSS-first configuration, design tokens, OKLCH colors, Vite setup, and dark-mode patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when setting up Tailwind CSS v4 projects, defining CSS-first theme tokens, choosing @theme modes, and configuring dark-mode behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Tailwind or Vite setup changes could be misapplied to projects that are not on the Tailwind v4 integration path.

Mitigation: Review package versions, Vite plugin wiring, and the CSS entry point before applying recommendations.

Risk: Package commands using @next may install prerelease packages when stable versions are expected.

Mitigation: Use @next only when prerelease packages are intended; otherwise pin stable Tailwind CSS v4 package versions.

Risk: Dark-mode SSR examples may not match an application's locale handling or security policy.

Mitigation: Adapt dark-mode snippets to the host application's SSR, locale, and security requirements before deployment.

## Reference(s):

- [Setup & Installation](artifact/references/setup.md)
- [Theming & Design Tokens](artifact/references/theming.md)
- [Dark Mode Strategies](artifact/references/dark-mode.md)
- [ClawHub Skill Page](https://clawhub.ai/anderskev/skills/tailwind-v4)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code blocks and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only output; no tool, persistence, or credential handling was identified in the security evidence.]

## Skill Version(s):

1.1.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
