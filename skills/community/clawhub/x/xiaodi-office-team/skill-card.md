## Description: <br>
An office secretary team skill for schedule management, email handling, document formatting, meeting minutes, and mind-map generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mx6315909](https://clawhub.ai/user/mx6315909) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and teams use this skill to draft office communications, organize schedules and meetings, format Markdown into office documents, generate meeting minutes and action items, and turn notes into mind maps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may process sensitive office data such as documents, meeting notes, email text, calendar content, and generated files. <br>
Mitigation: Use explicit prompts, provide only the confidential data needed for the task, and review generated files before sharing them. <br>
Risk: The release asks for broad file and command authority without enough scoping, consent, or safety controls. <br>
Mitigation: Prefer deployments that scope file paths, remove broad exec access where possible, and require confirmation before scheduling, email, or file-writing actions. <br>
Risk: Generated meeting minutes, replies, schedules, and document formatting may be incorrect or misleading. <br>
Mitigation: Treat outputs as drafts and verify facts, deadlines, recipients, and document formatting before operational use. <br>
Risk: Retention and cleanup behavior for generated files and office data is not clearly documented in the evidence. <br>
Mitigation: Define retention expectations before use and clean up generated files containing sensitive content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mx6315909/xiaodi-office-team) <br>
- [Publisher profile](https://clawhub.ai/user/mx6315909) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown text, email drafts, meeting-minute documents, Mermaid/PlantUML/Markmap code, shell command examples, JSON-style configuration, and generated DOCX/HTML/Markdown files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include generated local files for meeting minutes, mind maps, and formatted documents; users should review generated content before sharing or acting on it.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
