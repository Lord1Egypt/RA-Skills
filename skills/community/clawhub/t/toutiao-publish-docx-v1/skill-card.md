## Description: <br>
Publishes Toutiao articles from a title, body text, optional images, or a fixed-directory DOCX import using a provided cookie header or saved session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlesliu-sap](https://clawhub.ai/user/charlesliu-sap) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content operators and automation agents use this skill to prepare or publish articles in the Toutiao creator backend from text, images, or DOCX files. It supports a safer draft-fill mode by default and can publish when the user explicitly enables publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to a Toutiao account session or cookie header. <br>
Mitigation: Treat cookie_header like a password, avoid placing it in shared prompts or logs, and rotate or refresh the session if exposure is suspected. <br>
Risk: The skill can publish posts when publishing is explicitly enabled. <br>
Mitigation: Review title, body, images, and imported DOCX content before setting publish=true; use the default fill-only mode for checks. <br>
Risk: Saved screenshots or artifact folders may contain draft content or account-visible information. <br>
Mitigation: Limit access to troubleshooting artifacts and remove them when they are no longer needed. <br>
Risk: Login challenges, risk controls, sliders, or captchas can interrupt account access. <br>
Mitigation: Do not attempt to bypass controls; use a valid session from a browser that has already completed required verification. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlesliu-sap/toutiao-publish-docx-v1) <br>
- [Publisher profile](https://clawhub.ai/user/charlesliu-sap) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and parameter descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces execution guidance for an agent; publishing is disabled by default unless publish=true is supplied.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
