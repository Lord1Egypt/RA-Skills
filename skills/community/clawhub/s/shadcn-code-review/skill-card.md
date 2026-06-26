## Description: <br>
Reviews shadcn/ui components for CVA patterns, composition with asChild, accessibility states, and data-slot usage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and code reviewers use this skill to review React components built with shadcn/ui, Radix primitives, Tailwind styling, and class-variance-authority patterns. It focuses findings on component composition, accessibility state handling, variant structure, and data-slot usage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review guidance can produce incorrect or overbroad findings if the reviewer does not inspect the actual component imports, wrappers, and source locations. <br>
Mitigation: Apply the skill's hard gates before reporting: cite file location evidence, check valid-pattern exemptions, and verify context-sensitive accessibility or Radix claims against the code. <br>
Risk: The skill references a separate review-verification-protocol skill that is outside this package. <br>
Mitigation: Inspect and apply the referenced review-verification-protocol skill before relying on the complete review workflow. <br>


## Reference(s): <br>
- [Shadcn Code Review on ClawHub](https://clawhub.ai/anderskev/shadcn-code-review) <br>
- [CVA Patterns](references/cva-patterns.md) <br>
- [Component Composition](references/composition.md) <br>
- [Accessibility Patterns](references/accessibility.md) <br>
- [data-slot Pattern](references/data-slot.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Guidance] <br>
**Output Format:** [Markdown review findings and guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings should include concrete file location evidence and pass the skill's hard-gate checks before being reported.] <br>

## Skill Version(s): <br>
1.1.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
