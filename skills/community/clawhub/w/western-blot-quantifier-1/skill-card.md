## Description: <br>
Automatically identify Western Blot gel bands, perform densitometric analysis, and calculate normalized values relative to loading controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers and developers use this skill to prototype Western blot band detection, densitometry, and loading-control normalization workflows from gel image inputs. The packaged outputs should be independently validated before scientific or operational reliance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review found that the skill materially overstates its implemented Western blot analysis capabilities. <br>
Mitigation: Treat results as prototype outputs; validate behavior on known test images and independently verify any normalized values before use. <br>
Risk: The skill executes local Python code and reads user-supplied image paths. <br>
Mitigation: Run it in an isolated Python environment with workspace-scoped inputs and review file paths before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aipoch-ai/western-blot-quantifier-1) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; packaged script emits plain text demo output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Artifact documentation advertises CSV exports and visualizations, but server security evidence says the packaged code does not implement the full advertised workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
