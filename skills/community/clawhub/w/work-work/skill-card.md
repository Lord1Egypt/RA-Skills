## Description: <br>
Academic review writer and formatting assistant for Chinese academic papers, including literature review formatting, reference checks, citation consistency checks, and Word document generation. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[xf280230439-netizen](https://clawhub.ai/user/xf280230439-netizen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and academic writers use this skill to check Chinese academic literature reviews, validate references and citations, generate review reports, and produce formatted Word documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Word generator auto-opens files through a shell command built from a user-controlled path, creating a local command-execution risk. <br>
Mitigation: Review the scripts before running them, avoid unusual or untrusted filenames, and disable or remove auto-open behavior where possible. <br>
Risk: Some repair workflows can directly modify manuscript source files. <br>
Mitigation: Run the skill only on copies of manuscripts and keep a backup before using repair or renumbering scripts. <br>
Risk: Deep reference checking can send reference metadata to Crossref. <br>
Mitigation: Use --deep-check only when sharing reference metadata with Crossref is acceptable. <br>


## Reference(s): <br>
- [Workflow Guide](references/workflow_guide.md) <br>
- [Features Checklist](references/features_checklist.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/xf280230439-netizen/work-work) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown reports, shell command guidance, YAML configuration, and generated DOCX files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some scripts write report files or DOCX files next to the input document; selected repair scripts can modify source files.] <br>

## Skill Version(s): <br>
3.3.0 (source: server release metadata and changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
