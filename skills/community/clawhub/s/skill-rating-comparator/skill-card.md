## Description: <br>
Generates multi-dimensional skill comparison reports that score similar skills across functionality, code quality, documentation, user feedback, update frequency, and installation ease. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rfdiosuao](https://clawhub.ai/user/rfdiosuao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to compare a target skill with similar ClawHub or GitHub skills and produce a concise scoring report with strengths, weaknesses, and recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review found that the skill may present synthetic and randomized comparison reports as real skill analysis. <br>
Mitigation: Treat reports as preliminary guidance and require visible evidence for each score or recommendation before using them for selection, procurement, or publication. <br>
Risk: The implementation includes placeholder discovery and scoring behavior for ClawHub and GitHub comparisons. <br>
Mitigation: Confirm that real platform discovery, deterministic scoring, and source-backed recommendation logic are implemented before relying on output in production workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rfdiosuao/skill-rating-comparator) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [package.json](artifact/package.json) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, guidance] <br>
**Output Format:** [Markdown comparison report with tables, scoring details, recommendation bullets, and radar chart data as JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scores are generated for six weighted dimensions; security evidence notes that reports may be synthetic or randomized unless backed by visible data sources.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json, skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
