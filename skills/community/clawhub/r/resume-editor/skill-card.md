## Description: <br>
Build, edit, and format professional resumes with PDF import, styled HTML/PDF export, multi-language output, interactive review, and theme customization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chijiang](https://clawhub.ai/user/chijiang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create, import, refine, validate, and export professional resumes or CVs through an AI agent workflow. It supports structured resume JSON, themed HTML/PDF output, multi-language labels, custom themes, and an editable browser review loop. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Editable preview mode can write changes back to resume.json through a local sync server, and generated HTML contains save credentials for that session. <br>
Mitigation: Use editable mode only when local write-back is acceptable, prefer --no-sync or Copy JSON for sensitive documents, and stop the sync server after use. <br>
Risk: Processing untrusted resume PDFs or photo URLs can expose the user to parser, dependency, or remote-content risk. <br>
Mitigation: Avoid untrusted PDFs and photo URLs, keep PDF dependencies pinned and updated, and review imported data before export. <br>
Risk: AI-assisted resume edits can introduce incorrect claims, inconsistent wording, or misleading emphasis. <br>
Mitigation: Review the structured resume JSON and final rendered output for factual accuracy, grammar, consistency, and region-appropriate presentation before use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/chijiang/skills/resume-editor) <br>
- [Resume schema](references/resume-schema.json) <br>
- [Resume data structure](references/data-structure.md) <br>
- [Customization](references/customization.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Natural-language guidance with JSON resume data, Markdown/code snippets, shell commands, and generated HTML or PDF resume files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local-first workflow; optional editable HTML can write changes back to resume.json through a local sync server.] <br>

## Skill Version(s): <br>
1.3.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
