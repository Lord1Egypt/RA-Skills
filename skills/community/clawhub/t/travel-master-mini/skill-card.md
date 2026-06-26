## Description: <br>
A minimal travel-planning parser that extracts trip details with local keyword matching and reports a seven-field convergence score. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[timo2026](https://clawhub.ai/user/timo2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents can use this skill to parse short Chinese travel requests into structured trip fields and determine whether enough information has been collected for planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is a lightweight heuristic parser, not a full itinerary planner. <br>
Mitigation: Review extracted fields and request missing details before relying on the output for travel planning. <br>
Risk: GAODE_API_KEY is declared optional, but current evidence does not show map API usage. <br>
Mitigation: Do not provide a map API key unless a future version implements and documents that integration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/timo2026/travel-master-mini) <br>
- [Declared source repository](https://gitee.com/timo2026/travel-master-mini) <br>
- [Artifact README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, code] <br>
**Output Format:** [Text responses with Python dictionary-style structured results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local keyword matching; no external dependencies are required by the current artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
