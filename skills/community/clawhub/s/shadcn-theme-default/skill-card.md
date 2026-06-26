## Description: <br>
Enforces the default shadcn/ui Neutral theme (black/white/gray) with OKLCH CSS variables, Tailwind v4 integration, and dark mode support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guifav](https://clawhub.ai/user/guifav) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and frontend engineers use this skill to apply and maintain the default shadcn/ui Neutral theme in web projects. It guides CSS variable setup, Tailwind integration, dark mode support, and theme-token-based component styling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may overwrite or replace existing custom theme values in CSS or Tailwind files. <br>
Mitigation: Review the agent's plan and diffs before accepting changes, especially in projects with custom colors or existing design tokens. <br>
Risk: Using OKLCH variables in a Tailwind v3 project, or HSL variables in a Tailwind v4 project, can break color rendering. <br>
Mitigation: Confirm the installed Tailwind version before applying theme variables and use the matching v3 or v4 configuration path. <br>
Risk: Optional npm or npx commands may install next-themes, shadcn/ui components, or related dependencies. <br>
Mitigation: Review package installation commands and generated files before execution and verify the stack-scaffold dependency if it is resolved automatically. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guifav/shadcn-theme-default) <br>
- [Source homepage](https://github.com/guifav/openclaw-skills) <br>
- [shadcn/ui schema](https://ui.shadcn.com/schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with CSS, TypeScript, Tailwind configuration, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or apply edits to styling and Tailwind configuration files; optional npm or npx commands may install theme-related packages or shadcn/ui components.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata; artifact/claw.json and artifact/CHANGELOG.md list 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
