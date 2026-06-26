## Description: <br>
A general data annotation skill for image, video, text, and mixed datasets that helps agents plan annotation work, call appropriate models, save structured results, and provide a web review and editing interface. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aowind](https://clawhub.ai/user/aowind) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data operations teams, and annotation reviewers use this skill to create and resume data-labeling workflows, generate JSONL annotation outputs from requirements and source data, and review or edit annotations through a web interface. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The web API and deployment guidance can expose private files or allow broad file writes if published without controls. <br>
Mitigation: Use only in a controlled environment; add authentication, remove wildcard CORS and autoindex, restrict reads and writes to a dedicated data directory, and avoid running the API as root. <br>
Risk: Annotation workflows may upload private data to third-party model APIs. <br>
Mitigation: Confirm that model-provider use is approved for the dataset before sending files or extracted content to external services. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/aowind/sjht-data-annotation) <br>
- [Output formats reference](references/output-formats.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration, JSONL files, HTML files] <br>
**Output Format:** [Markdown guidance with JSON, JSONL, shell, Python, HTML, and nginx configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces annotation plans, progress updates, dataset JSONL records, summary JSON, and optional web viewer/API deployment assets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
