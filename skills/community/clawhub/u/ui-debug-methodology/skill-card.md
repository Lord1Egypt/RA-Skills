## Description:

UI/front-end debugging methodology that makes agents inspect CSS, layout, and component behavior before changing code, reducing blind trial-and-error.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrsh44e](https://clawhub.ai/user/chrsh44e)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineering agents use this skill when debugging frontend UI behavior, CSS, layout, or component interaction issues. It guides them through observing runtime behavior, understanding the mechanism, finding the root cause, making the smallest fix, and verifying related scenarios.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger wording may cause the workflow to activate for many frontend issues and slow down simple fixes.

Mitigation: Apply it when UI behavior, CSS, layout, or component interaction debugging is needed, and keep the investigation focused on the five-step workflow.

Risk: Skipping runtime observation or final verification could preserve an incorrect diagnosis or incomplete UI fix.

Mitigation: Use DevTools or Playwright to inspect the actual DOM, styles, and behavior before editing, then verify the original issue and related scenarios after the fix.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chrsh44e/skills/ui-debug-methodology)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Code]

**Output Format:** [Markdown with checklists and JavaScript Playwright snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable files; the skill provides a frontend debugging workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
