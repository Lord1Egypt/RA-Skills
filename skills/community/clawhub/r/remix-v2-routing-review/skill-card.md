## Description: <br>
Reviews Remix v2 route files for naming convention violations, missing layouts, resource-route shape, and v1 holdovers. Use when reviewing files under app/routes/ in a Remix v2 codebase. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and code reviewers use this skill to review Remix v2 routing files for route naming, layout outlet, resource route, root shell, and v1 migration issues before reporting findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may suggest routing fixes that are incorrect if the reviewer has not confirmed Remix v2 routing mode, v1-route-convention adapter status, or route-specific exemptions. <br>
Mitigation: Follow the skill's version, exemption, and location-evidence gates before reporting findings, and review suggested code changes before applying them. <br>


## Reference(s): <br>
- [Remix V2 Routing Review on ClawHub](https://clawhub.ai/anderskev/remix-v2-routing-review) <br>
- [Route Files](references/route-files.md) <br>
- [Layouts and Outlets](references/layouts-outlets.md) <br>
- [Resource Routes](references/resource-routes.md) <br>
- [Root Shell Smells](references/root-shell.md) <br>
- [V1 Holdovers](references/v1-holdovers.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Guidance] <br>
**Output Format:** [Markdown review findings with file evidence, explanations, and suggested fixes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings should be reported only after the skill's pre-report verification gates pass.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
