## Description: <br>
Analyze OpenClaw skill ecosystems by mapping dependencies, detecting orphan skills, scoring ecosystem health, and answering impact questions about skill relationships. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjipeng977](https://clawhub.ai/user/wangjipeng977) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use Skill Net to inspect an OpenClaw skill ecosystem, identify dependency relationships, find skills without trigger phrases, and understand what may be affected by removing or changing a skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads installed SKILL.md files and can save derived dependency reports that may reflect private skill instructions. <br>
Mitigation: Run it only in workspaces where local skill instructions may be inspected, and review or delete generated reports before sharing them. <br>
Risk: Dependency and deletion-impact results are diagnostic estimates based on detected references, so they may overstate or understate actual runtime coupling. <br>
Mitigation: Use the report as a review aid and confirm high-impact changes against the affected skills before modifying or deleting anything. <br>


## Reference(s): <br>
- [ClawHub Skill Net listing](https://clawhub.ai/wangjipeng977/skill-net) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>
- [Analyzer script](artifact/scripts/analyze_deps.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown report, JSON data, and terminal output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save derived local reports such as data/ecosystem.json and data/report.md during analysis.] <br>

## Skill Version(s): <br>
3.1.0 (source: server release metadata; README badge agrees) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
