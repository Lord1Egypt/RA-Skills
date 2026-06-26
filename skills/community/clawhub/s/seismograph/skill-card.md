## Description: <br>
Predicts the ripple effects of a proposed change before you make it by mapping how a modification propagates through code, tests, contracts, configuration, and downstream systems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jcools1977](https://clawhub.ai/user/jcools1977) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use Seismograph before code changes and during PR review to map direct, indirect, and side-effect impacts across interfaces, tests, documentation, configuration, and downstream systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill analyzes repository content and may be invoked during ordinary engineering discussion because of its broad change-impact posture. <br>
Mitigation: Use it on repositories you are comfortable letting an agent read, and scope requests to concrete proposed changes, interfaces, or pull requests. <br>
Risk: Impact reports are advisory and may contain incorrect or overbroad recommendations. <br>
Mitigation: Review the analysis before changing code, especially for public interfaces, schemas, wire formats, and downstream integrations. <br>


## Reference(s): <br>
- [Seismograph on ClawHub](https://clawhub.ai/jcools1977/seismograph) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Guidance, Markdown] <br>
**Output Format:** [Markdown report with structured impact analysis] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Advisory output; no API calls or external dependencies are indicated by the release evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
