## Description: <br>
Scans Vue2 projects for dependency security issues, risky Webpack settings, and Babel configuration problems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gfrxf](https://clawhub.ai/user/gfrxf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers working on Vue2 projects use this skill to run local or CI checks for dependency vulnerabilities, Webpack source-map or eval risks, and Babel polyfill or core-js configuration issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs shell scripts and npm audit commands in the current project directory. <br>
Mitigation: Review the scripts before use and run them only from the intended Vue2 project root or a controlled CI job. <br>
Risk: The checks are heuristic and may miss issues outside the declared dependency, Webpack, and Babel patterns. <br>
Mitigation: Treat the output as a triage aid and confirm findings with standard dependency, build, and security review workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gfrxf/vue2-risk-scan) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Terminal text with high and medium risk counts plus individual flagged findings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs dependency, Webpack, and Babel checks from the project root; no structured JSON output is declared.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
