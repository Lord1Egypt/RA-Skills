## Description: <br>
Autonomous space navigation agent using optical quantum kernels for terrain classification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AadiPapp](https://clawhub.ai/user/AadiPapp) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers can use this skill to simulate terrain classification from sensor vectors and receive proceed, avoid, halt, or safe-mode navigation recommendations for a toy or research-style space autonomy workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The space-navigation framing could be mistaken for validated autonomous navigation capability. <br>
Mitigation: Use it only as a toy or research-style terrain classification helper, and require independent validation, explicit guardrails, and human review before any safety-critical use. <br>
Risk: Classifier confidence and printed navigation decisions may be misleading for real spacecraft, robotics, rover, drone, vehicle, or other safety-critical systems. <br>
Mitigation: Do not rely on the generated decisions for real navigation; treat them as local simulation output for review and experimentation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AadiPapp/space-autonomy-skill) <br>
- [README](README.md) <br>
- [Navigation script](scripts/quantum_nav.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text command-line output and Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Takes a comma-separated numeric sensor vector and prints terrain scores plus a navigation decision.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
