## Description: <br>
Transforms simulated mmWave radar phase data into pet health metrics by filtering respiration signals, generating diagnostic charts, and combining results with environmental data for pet welfare actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SpaceSQ](https://clawhub.ai/user/SpaceSQ) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to evaluate a pet-health sensing pipeline that synthesizes mmWave radar data, extracts respiration metrics, renders a diagnostic chart, and emits environmental adjustment intent. It is suited for agent workflows that need text guidance, runnable Python, and generated analysis artifacts around pet welfare monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary reports clean scan signals but notes that full artifact-backed review was not available to the scanner. <br>
Mitigation: Review the visible skill files, dependency list, and requested runtime permissions before deployment, and re-run security checks in the target environment. <br>
Risk: The skill simulates radar and environment data, so generated health conclusions may not reflect a real animal or hardware deployment. <br>
Mitigation: Treat outputs as development diagnostics unless validated with real sensors, domain review, and appropriate pet health oversight. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/SpaceSQ/s2-pet-mmwave-analyzer) <br>
- [Project Homepage](https://space2.world) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions, Python code, shell commands, console text, and generated PNG chart output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a local s2_pet_health_vault directory and writes pet_vital_radar_report.png when the Python pipeline is executed.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and manifest.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
