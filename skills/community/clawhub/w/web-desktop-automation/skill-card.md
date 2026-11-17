## Description:

Use when the user wants browser automation, web scraping, form filling, clicking, or desktop GUI automation, including mixed workflows that move between web pages and local applications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lurui808](https://clawhub.ai/user/lurui808)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to plan and run supervised browser, desktop, and mixed browser-to-desktop workflows such as scraping, form filling, downloads, local app actions, and uploads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can enable login flows, file transfers, screenshots, form submissions, uploads, and desktop typing or clicking.

Mitigation: Use it only for supervised browser and desktop automation, and clearly approve the exact action and target before sensitive or irreversible steps.

Risk: Desktop automation may act on the wrong window, field, or coordinates when UI state changes.

Mitigation: Verify the active page or window after each phase, prefer stable selectors or application-aware controls, and stop before actions that risk data loss.

Risk: The automation dependencies expand the local execution surface.

Mitigation: Install in an isolated virtual environment, pin and review dependencies before production use, and install only when supervised browser plus desktop automation is needed.

## Reference(s):

- [Browser Workflows](references/browser-workflows.md)
- [Desktop Workflows](references/desktop-workflows.md)
- [Mixed Flows](references/mixed-flows.md)
- [Real-World Mixed Example](references/mixed-example.md)
- [Dependencies and Installation](references/dependencies.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with Python code templates and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce supervised browser, desktop, or mixed automation plans and scripts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
