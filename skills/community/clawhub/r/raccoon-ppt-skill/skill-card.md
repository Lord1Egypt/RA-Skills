## Description: <br>
Raccoon PPT creates new presentation decks from a natural-language topic through the PPT OpenAPI and can continue or check an existing PPT generation task. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raccoon-office](https://clawhub.ai/user/raccoon-office) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and agents use this skill to create a complete PPT deck from a topic, collect required presentation parameters, continue service follow-up questions, and return the final download link or failure reason. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Presentation prompts and generated content are sent to a remote PPT generation API. <br>
Mitigation: Use only with content approved for that service; avoid confidential, regulated, investor, or internal material unless the service is approved for that data. <br>
Risk: Local output files may retain prompts, task records, or download links after generation. <br>
Mitigation: Periodically delete saved output files when prompts or links should not remain on disk. <br>
Risk: The skill depends on a bearer token and a remote service, so failed authentication or service errors can interrupt generation. <br>
Mitigation: Confirm RACCOON_API_TOKEN is set, keep the token private, and retry or report user-friendly service errors when the API cannot complete the task. <br>


## Reference(s): <br>
- [Raccoon PPT Skill on ClawHub](https://clawhub.ai/raccoon-office/raccoon-ppt-skill) <br>
- [raccoon-office Publisher Profile](https://clawhub.ai/user/raccoon-office) <br>
- [Raccoon Homepage](https://xiaohuanxiong.com) <br>
- [PPT OpenAPI Skill Reference](references/API_REFERENCE.md) <br>
- [API Cheatsheet](references/CHEATSHEET.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files, Guidance] <br>
**Output Format:** [Text or Markdown guidance with shell commands, task status messages, download links, and generated PPT files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 plus RACCOON_API_TOKEN; RACCOON_API_HOST is optional and defaults to the Raccoon service.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
