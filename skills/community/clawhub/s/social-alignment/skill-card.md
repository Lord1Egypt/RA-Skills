## Description: <br>
Five-lens ethical compass for sovereign AI agents - evaluate actions across trust, ownership, defense, and sovereignty before proceeding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vveerrgg](https://clawhub.ai/user/vveerrgg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and their operators use this skill to check significant actions through five alignment lenses before proceeding, escalating to a human when risk, uncertainty, or trust concerns are high. It supports setup, day-to-day action checks, outcome tracking, and optional local decision memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and imports an external Python package before use. <br>
Mitigation: Verify the social-alignment package and test it in an isolated environment before relying on it. <br>
Risk: Optional persistent decision memory may reveal patterns about operator decisions. <br>
Mitigation: Enable persistence only in a controlled local file path and apply appropriate file permissions. <br>
Risk: Alignment checks depend on accurate context about confidence, reversibility, money, secrets, and trust boundaries. <br>
Mitigation: Provide honest action context and escalate when the result indicates YIELD or STOP. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/vveerrgg/social-alignment) <br>
- [GitHub Homepage](https://github.com/HumanjavaEnterprises/nostralignment.app.OC-python.src) <br>
- [PyPI Package](https://pypi.org/project/social-alignment/) <br>
- [NSE Platform](https://nse.dev) <br>
- [NostrKey](https://clawhub.ai/vveerrgg/nostrkey) <br>
- [sense-memory](https://clawhub.ai/vveerrgg/sense-memory) <br>
- [NSE Orchestrator](https://clawhub.ai/vveerrgg/nse) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Analysis, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce human escalation messages, action-check rationale, and local decision-memory setup guidance.] <br>

## Skill Version(s): <br>
0.1.5 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
