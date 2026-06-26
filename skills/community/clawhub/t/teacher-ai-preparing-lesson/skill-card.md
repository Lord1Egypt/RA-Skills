## Description: <br>
中小学教师智能备课助手，可为中小学教师生成课件、教学设计、学生任务单、参考资源清单和辅助教学 HTML 工具。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ahao2001](https://clawhub.ai/user/ahao2001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Teachers use this skill to prepare complete K-12 lesson materials for subjects such as Chinese, mathematics, and English. It helps an agent collect lesson details, create course folders, draft PPT and Word-ready lesson assets, generate supporting HTML tools and mind maps, and organize reference resources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Education-platform account passwords are stored in plaintext local JSON. <br>
Mitigation: Skip account setup or use only credentials acceptable for plaintext workspace storage; restrict workspace access and remove the account JSON when no longer needed. <br>
Risk: The skill creates workspace folders, downloads external resources, and makes persistent configuration changes. <br>
Mitigation: Install and run it only in a workspace where automatic file creation and downloads are acceptable, then review generated files and resource lists before reuse. <br>
Risk: Broad cleanup guidance for .py and .js files could remove unrelated files if applied outside the generated lesson folder. <br>
Mitigation: Constrain cleanup to the generated lesson output directory and confirm paths before deleting script files. <br>
Risk: Global activation aliases may trigger the skill when the user intended a different workflow. <br>
Mitigation: Remove or narrow unnecessary aliases in the user's global memory or launcher configuration. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ahao2001/teacher-ai-preparing-lesson) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>
- [Installation guide](artifact/INSTALL.md) <br>
- [Teaching design template](artifact/references/teaching_design_template_v2.md) <br>
- [Student task sheet template](artifact/references/task_sheet_template_v2.md) <br>
- [PPT guide](artifact/references/ppt_guide.md) <br>
- [Mind map guide](artifact/references/mindmap_guide.md) <br>
- [Education platforms reference](artifact/references/edu_platforms.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with generated document data, file paths, shell commands, configuration prompts, and lesson-material file outputs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create workspace folders under MyTeacher and local account configuration under .workbuddy when used.] <br>

## Skill Version(s): <br>
2.1.1 (source: ClawHub release metadata; artifact frontmatter reports 2.1.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
