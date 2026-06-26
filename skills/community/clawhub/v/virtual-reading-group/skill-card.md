## Description: <br>
Orchestrates a multi-agent virtual academic reading group that reads academic papers, creates expert notes, cross-examines interpretations, and synthesizes cited discussion summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[IsonaEi](https://clawhub.ai/user/IsonaEi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Researchers, analysts, and agent users use this skill to run a structured reading-group workflow over 1-50 academic papers, producing traceable notes, discussion questions, expert responses, and a thematic synthesis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow reads user-selected papers and writes multiple Markdown outputs, so a shared or cluttered output folder can mix unrelated private files with generated notes. <br>
Mitigation: Use a fresh output folder for each run and avoid placing unrelated private files in that folder. <br>
Risk: Intermediate notes or citations can be incomplete or misleading if source passages are missing or not reviewed. <br>
Mitigation: Review intermediate notes and citations before relying on the final synthesis. <br>
Risk: This is a multi-agent reading-group workflow and may be excessive for users who only need a simple paper summary. <br>
Mitigation: Install and invoke it only when the reading-group workflow is desired. <br>


## Reference(s): <br>
- [Workflow Specification](references/workflow.md) <br>
- [Default Personas](references/default-personas.md) <br>
- [Paper Notes Template](references/paper-notes-template.md) <br>
- [Synthesis Template](assets/synthesis-template.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/IsonaEi/virtual-reading-group) <br>
- [Publisher Profile](https://clawhub.ai/user/IsonaEi) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown files and a concise completion summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes paper notes, expert session summaries, junior discussion, expert responses, and an integrated discussion summary into a user-selected output directory.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
