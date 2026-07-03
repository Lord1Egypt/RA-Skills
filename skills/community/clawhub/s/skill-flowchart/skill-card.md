## Description: <br>
SkillFlowChart helps an agent turn natural-language skill definitions into structured nodes and self-contained HTML decision flowcharts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codermoray](https://clawhub.ai/user/codermoray) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to document skill execution logic, decision trees, and workflows as readable flowcharts. The agent extracts a nodes.json structure from a SKILL.md-style definition, then the bundled Python renderer produces deterministic HTML/SVG output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated flowchart can reflect mistakes in the agent-extracted nodes.json structure. <br>
Mitigation: Review nodes, edges, labels, and loops before rendering or publishing the HTML output. <br>
Risk: The renderer writes files to the output path supplied by the user. <br>
Mitigation: Choose output paths deliberately and avoid overwriting important local files. <br>
Risk: Bundled HaluCatch and security-review documents may be mistaken for runtime authority. <br>
Mitigation: Treat bundled documents as examples for flowchart structure, not as operational instructions for SkillFlowChart. <br>


## Reference(s): <br>
- [ClawHub SkillFlowChart page](https://clawhub.ai/codermoray/skills/skill-flowchart) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Flowchart renderer](artifact/scripts/flowchart.py) <br>
- [HaluCatch example nodes](artifact/docs/halucatch-nodes.json) <br>
- [Security review example nodes](artifact/docs/security-review-nodes.json) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, HTML files, Shell commands, Guidance] <br>
**Output Format:** [Structured nodes.json plus self-contained HTML/SVG flowchart files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The renderer is a local Python script that uses the standard library and writes to the requested output path.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
