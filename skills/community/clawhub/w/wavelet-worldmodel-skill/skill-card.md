## Description: <br>
Generates a world model representation from state inputs using discrete wavelet transforms (DWT) to capture multi-resolution temporal and spatial features. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AadiPapp](https://clawhub.ai/user/AadiPapp) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and robotics or reinforcement-learning engineers can use this skill to transform high-dimensional sequential state data into a compact multi-resolution representation for downstream control, tracking, or predictive workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper depends on PyWavelets for local wavelet processing. <br>
Mitigation: Install PyWavelets from a trusted package index and pin dependency versions when reproducibility or supply-chain control matters. <br>
Risk: The compressed state vector may be unsuitable for a downstream model or control task without validation on representative state history. <br>
Mitigation: Validate output shape, reconstruction behavior, and task performance before using the representation in control, tracking, or prediction workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AadiPapp/wavelet-worldmodel-skill) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/AadiPapp) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance and Python command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a compressed state vector from local wavelet processing when the Python helper is run with sufficient state history.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
