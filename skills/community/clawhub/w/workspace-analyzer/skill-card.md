## Description: <br>
Analyzes OpenClaw workspace structure and content to identify maintenance needs, bloat, duplicates, and organization issues. Outputs a JSON report for the agent to review and act upon. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zendenho7](https://clawhub.ai/user/zendenho7) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw workspace maintainers use this skill to inspect workspace structure, detect maintenance issues such as bloat and duplicate content, and produce an actionable JSON report for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workspace reports may expose file paths, structure, and maintenance metadata if stored or shared carelessly. <br>
Mitigation: Keep the scan root narrow and handle generated JSON reports as potentially sensitive workspace metadata. <br>
Risk: The bundled run script writes its default report to a fixed path under /tmp, which may be undesirable on shared machines. <br>
Mitigation: Use an explicit output path in a private workspace when privacy matters, and remove temporary reports after review. <br>
Risk: The skill can suggest edits or commits for agents to perform after analysis. <br>
Mitigation: Review recommendations before allowing an agent to modify core files or create git commits. <br>


## Reference(s): <br>
- [Workspace Analyzer ClawHub page](https://clawhub.ai/zendenho7/workspace-analyzer) <br>
- [Publisher profile](https://clawhub.ai/user/zendenho7) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, JSON report, Guidance] <br>
**Output Format:** [JSON report with summary and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports workspace file metadata, detected core files, issue findings, single-source validation, and recommendations.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
