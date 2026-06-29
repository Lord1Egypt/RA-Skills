## Description: <br>
Create or revise document, PDF, web, or review images with the requested format, sharp raster output, and artifact validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xrowgmbh](https://clawhub.ai/user/xrowgmbh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to create, revise, regenerate, and review image assets for Markdown, PDF, DOCX, web pages, merge requests, and release artifacts while preserving requested formats and validating outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may lead an agent to create or update image files and rebuild downstream documents in a repository. <br>
Mitigation: Review generated image artifacts and downstream Markdown, PDF, DOCX, web, or release changes before committing or publishing. <br>
Risk: Generated image outputs can drift from the requested format, resolution, or style if the agent does not validate the final artifact. <br>
Mitigation: Validate the actual output extension, MIME format, dimensions, DPI metadata when relevant, and generated sibling freshness before final review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xrowgmbh/skills/xrowgmbh-image-generation) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with file paths, validation commands, and generated artifact notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update image files and related documentation artifacts when the agent applies the workflow.] <br>

## Skill Version(s): <br>
1.62.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
