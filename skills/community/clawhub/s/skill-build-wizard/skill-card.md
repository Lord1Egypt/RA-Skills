## Description: <br>
Skill Build Wizard guides agents and users through a four-stage workflow for building production-quality agent skills, from pre-flight checks through release preparation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[songhonglei](https://clawhub.ai/user/songhonglei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use this skill to structure skill creation, confirm requirements before coding, run acceptance checks, and prepare releases with explicit user approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can guide an agent through file creation and eventual skill publication, so unreviewed steps could release incorrect or unintended changes. <br>
Mitigation: Review and explicitly approve the design, acceptance report, version, changelog, and publish confirmation before allowing release steps. <br>
Risk: Workspace changes may be difficult to recover if the build starts without version control or continuity planning. <br>
Mitigation: Run the pre-flight checks, use a version-controlled workspace, and save design context before coding begins. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/songhonglei/skill-build-wizard) <br>
- [Pre-flight Checklist](references/checklist-before-start.md) <br>
- [Coding Acceptance Checklist](references/checklist-coding.md) <br>
- [Release Prep Checklist](references/checklist-release.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user confirmation before stage handoffs and release publication.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact documentation) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
