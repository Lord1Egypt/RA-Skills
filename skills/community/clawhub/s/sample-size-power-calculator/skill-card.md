## Description: <br>
Advanced sample size and power calculations for complex study designs including survival analysis, clustered designs, and multiple comparisons. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, analysts, and developers use this skill to run local sample size and power estimates for supported statistical tests and document assumptions for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release may overstate advanced power-analysis capabilities compared with the implemented local calculator. <br>
Mitigation: Treat outputs as preliminary planning estimates, verify formulas and assumptions independently, and do not rely on it as a validated clinical or regulated study-planning package. <br>
Risk: Dependency versions are not pinned, which can affect reproducibility and numerical behavior. <br>
Mitigation: Pin and audit numpy and scipy versions before relying on results in scientific, clinical, or regulated study planning. <br>


## Reference(s): <br>
- [Audit Reference](references/audit-reference.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/sample-size-power-calculator) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and plain-text calculation results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-supplied statistical design parameters; results should be independently verified before regulated use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
