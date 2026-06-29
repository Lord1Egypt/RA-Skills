## Description: <br>
Detects structural holes, hidden dependencies, and missing links in directed networks using eigenvalue decomposition of a combined adjacency and similarity matrix. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evezart](https://clawhub.ai/user/evezart) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to apply spectral graph analysis to directed networks, identify structural gaps, and inspect candidate missing links or hidden dependencies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill references a local topology_engine.py implementation that is not included in the submitted artifact. <br>
Mitigation: Inspect and trust the referenced local implementation before installing or using it. <br>


## Reference(s): <br>
- [Submitted skill artifact](artifact/SKILL.md) <br>
- [ClawHub skill page](https://clawhub.ai/evezart/skills/spectral-topology) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code] <br>
**Output Format:** [Markdown with Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe TopologyReport summaries, JSON export behavior, and StructuralGap fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
