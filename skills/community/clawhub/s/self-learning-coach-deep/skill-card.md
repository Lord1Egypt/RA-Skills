## Description: <br>
Self Learning Coach Deep guides AI agents through quick, standard, or deep learning paths, generating source-grounded HTML lessons, business-context analysis, practice tasks, progress tracking, and source records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zzj997](https://clawhub.ai/user/zzj997) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external learners, and developers use this skill with capable agents to turn user-provided materials, web sources, or Feishu/internal documents into structured lessons that connect concepts to business scenarios and practice. It is especially suited to guided self-learning, case diagnosis, and training-material style lesson generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lesson files and source records may include sensitive content from user-provided Feishu or local materials. <br>
Mitigation: Use approved materials only, review generated lesson and source files before sharing, and avoid exposing private links, local paths, or permission-sensitive metadata. <br>
Risk: Generated learning content may contain incorrect or misleading explanations, citations, or business recommendations. <br>
Mitigation: Review source grounding, inline markers, and case analysis before relying on the lesson for training or operational decisions. <br>
Risk: When used in Feishu-capable environments, generated HTML may be sent to a chat or recipient selected by the agent workflow. <br>
Mitigation: Confirm the intended channel or recipient and inspect generated HTML before delivery when sensitive material is involved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zzj997/skills/self-learning-coach-deep) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown chat responses, self-contained HTML lesson files, and Markdown tracking tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates lesson files under lessons/, updates LEARNING_STATUS.md and LEARNING_SOURCES.md, and may use Feishu file delivery when available.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
