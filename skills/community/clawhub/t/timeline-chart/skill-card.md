## Description: <br>
Professional timeline chart generator with Chinese/number support and dynamic layout. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[austin0208](https://clawhub.ai/user/austin0208) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate professional PNG timeline charts for project milestones, historical events, process flows, milestone showcases, and decision flows, including timelines with Chinese text, numbers, and punctuation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes generated chart images to a caller-provided local output path. <br>
Mitigation: Review or choose the output path before running the generator. <br>
Risk: The chart generator depends on local Pillow and CJK font packages for correct rendering. <br>
Mitigation: Install Pillow and the listed font packages only from trusted package sources. <br>


## Reference(s): <br>
- [Timeline Chart Generator on ClawHub](https://clawhub.ai/austin0208/timeline-chart) <br>


## Skill Output: <br>
**Output Type(s):** [code, shell commands, configuration, guidance] <br>
**Output Format:** [Python code and Markdown guidance for generating PNG image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local PNG timeline chart files; requires Python, Pillow, and suitable CJK fonts for Chinese text rendering.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, skill.json, and SKILL.md version history) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
