## Description: <br>
Basic sample size calculator for clinical research planning with common statistical scenarios. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External researchers, clinicians, and study-design teams use this skill to estimate preliminary sample sizes for grant proposals, study planning, and statistics education. Outputs should be treated as planning aids for qualified review, not clinical advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The calculator can produce misleading planning estimates if inputs or statistical assumptions are wrong. <br>
Mitigation: Use results as preliminary planning aids and have a qualified reviewer verify assumptions before relying on them for clinical research decisions. <br>
Risk: Unpinned numpy and scipy dependencies may change behavior across environments. <br>
Mitigation: Install in a virtual environment and pin reviewed dependency versions or use a lockfile for reproducible execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aipoch-ai/sample-size-basic) <br>
- [Publisher profile](https://clawhub.ai/user/aipoch-ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text CLI output with sample size estimates and statistical assumptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns required sample size per group, total sample size, and summary text for supported statistical scenarios.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
