## Description: <br>
A multi-agent workflow for MBA and academic thesis writing that coordinates outline planning, node-by-node drafting, review loops, research search, and Word export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hehe973781230](https://clawhub.ai/user/hehe973781230) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to manage the full lifecycle of MBA or academic thesis drafting, review, revision, and Word export. It is especially suited to long-form academic writing workflows that need outline anchoring, human checkpoints, citation checks, and final formatting validation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Thesis documents, company names, and research topics may be shared with search providers, LLM providers, or optional parsing services. <br>
Mitigation: Use a separate workspace for confidential work, remove sensitive identifiers when possible, and disable optional network or parsing components that are not required. <br>
Risk: The workflow may access local OpenClaw credentials and install dependencies during setup or preflight. <br>
Mitigation: Review installation steps before running them, use an isolated environment, and confirm that credential and package-installation access is acceptable. <br>
Risk: Generated academic content and citations may be incomplete, misleading, or unsuitable for submission without review. <br>
Mitigation: Keep the human-in-the-loop checkpoints enabled and independently verify sources, citations, formatting, and institutional requirements before final delivery. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hehe973781230/skills/thesis-workflow-v2) <br>
- [README_EN.md](README_EN.md) <br>
- [Academic Standards Checklist](references/checklist.md) <br>
- [Loop Design](references/loop-design.md) <br>
- [Chapter Summary Design](references/chapter-summary-design.md) <br>
- [Git Workflow](references/git-workflow.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown thesis drafts, review reports, structured workflow status, shell command guidance, and DOCX files produced by the workflow scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include intermediate state files, outline data, review findings, and final Word documents.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
