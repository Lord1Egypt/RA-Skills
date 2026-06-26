## Description: <br>
Generate font-based signature images via Signus API and return image files for chat delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[signus-ai](https://clawhub.ai/user/signus-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to request font-based signature image variations from Signus using a name, first and last name, or initials, then return generated image files for chat delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends provided identity text to Signus for signature generation. <br>
Mitigation: Use only ordinary names or initials and install only when sending that identity text to Signus is acceptable. <br>
Risk: Path-like identity input can write generated files outside the promised output folder. <br>
Mitigation: Avoid path-like input and enforce resolved-path containment under the intended output directory before deployment. <br>
Risk: Generated signature images are kept on disk. <br>
Mitigation: Review local retention expectations and remove generated files when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/signus-ai/signus-font-signature) <br>
- [Publisher profile](https://clawhub.ai/user/signus-ai) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Images, JSON] <br>
**Output Format:** [JSON object with count, directory, and signatures array plus generated image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated signature files are written under the skill's media output directory for chat delivery.] <br>

## Skill Version(s): <br>
1.0.1 (source: package.json and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
