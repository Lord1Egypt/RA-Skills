## Description: <br>
Generate a link to an interactive 3D decision wheel that randomly chooses among 2 to 20 user-provided options with optional weights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[peetzweg](https://clawhub.ai/user/peetzweg) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill when a user wants a playful random choice among concrete options rather than a reasoned recommendation. The agent collects the options, builds a URL with encoded labels and optional weights, and returns the link for the user to open. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Option labels are placed in a URL opened on an external website, which can expose confidential names, private business options, personal data, or sensitive decisions. <br>
Mitigation: Use only non-sensitive option labels and avoid confidential, personal, or sensitive decision content when creating the wheel link. <br>
Risk: The skill is intended for random selection and may be inappropriate for decisions that require judgment, safety review, or a reasoned recommendation. <br>
Mitigation: Use the skill only when randomness is explicitly welcome and provide reasoned guidance instead for consequential choices. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/peetzweg/wheel-of-fortune) <br>
- [Decision wheel web app](https://makedecisionforme.netlify.app/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown response containing a generated URL] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The URL contains user-provided option labels and optional integer weights; labels should be URL-encoded.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
