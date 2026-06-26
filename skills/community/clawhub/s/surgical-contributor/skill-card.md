## Description: <br>
Deliver small, high-signal repository fixes by reproducing one real pain point, applying the narrowest safe change, adding regression protection, and writing a maintainer-friendly PR summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dj-shortcut](https://clawhub.ai/user/dj-shortcut) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to make small, reviewable bug fixes or workflow paper-cut improvements with a reproduced issue, focused regression protection, and a maintainer-ready PR summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to modify project files and tests, so an incorrect patch could change repository behavior. <br>
Mitigation: Review the resulting diff and verification output before committing, merging, or publishing changes. <br>
Risk: A selected pain point may be underspecified or incorrectly reproduced, leading to a narrow fix that does not address the intended problem. <br>
Mitigation: Require a minimal reproduction, explicit assumptions, and one focused regression protection tied to the observed issue. <br>


## Reference(s): <br>
- [Risk Map](references/risk-map.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown response with concise analysis, file-edit summaries, verification commands, and PR summary text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May modify repository files and tests as part of a narrow, verified fix.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
