## Description: <br>
Skill Release Audit is a report-only static auditor that checks AI agent skill packages for syntax, feature coverage, edge-case handling, data-safety, dependency, and documentation issues before release. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[songhonglei](https://clawhub.ai/user/songhonglei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use it as a pre-publish gate for SKILL.md-based agent skills. It produces structured findings and suggested fixes without editing or publishing the target skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional dependency installer can fetch and execute packages inferred from a skill being audited. <br>
Mitigation: Avoid --auto-install unless the audited skill is trusted; review install commands first and use an isolated environment. <br>
Risk: Audit findings and suggested fixes may be incomplete or require judgment before changing a skill. <br>
Mitigation: Review the full report before acting and require explicit confirmation before modifying files. <br>


## Reference(s): <br>
- [Dependency Detection Patterns](references/dep-patterns.md) <br>
- [Skill Registry / Hub Specifications](references/hub-specs.md) <br>
- [Portable Safe Paths for Skill Data](references/safe-paths.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-style terminal report with module findings and suggested fixes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Report-only by default; optional dependency installation is enabled only when requested.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata and SKILL.md body) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
