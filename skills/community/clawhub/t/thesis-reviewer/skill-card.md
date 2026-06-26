## Description: <br>
Use when the user wants to review, evaluate, or provide feedback on a master's or doctoral thesis across multiple academic disciplines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agents365-ai](https://clawhub.ai/user/agents365-ai) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Students, supervisors, and academic reviewers use this skill to convert a thesis document, inspect structure and discipline-specific quality criteria, and generate actionable review feedback before submission. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow includes silent self-update instructions that can change installed skill instructions before review. <br>
Mitigation: Remove or disable silent auto-update behavior, or require explicit approval from a pinned, trusted source before updating. <br>
Risk: Thesis documents may contain confidential, unpublished, or human-subject information, and converted Markdown plus review reports are saved beside the source file. <br>
Mitigation: Process only material approved for the local environment, use a trusted local conversion server where possible, and protect generated Markdown and report files. <br>
Risk: Markdown conversion can miss formatting details such as page layout, headers, image resolution, and other document-level presentation issues. <br>
Mitigation: Verify formatting-sensitive findings against the original thesis document before relying on the review. <br>
Risk: Automated thesis review feedback may be incomplete or academically inappropriate for a specific institution, discipline, or committee. <br>
Mitigation: Have a qualified supervisor or reviewer check the generated feedback before using it for academic decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/agents365-ai/thesis-reviewer) <br>
- [Publisher Profile](https://clawhub.ai/user/agents365-ai) <br>
- [Skill Homepage](https://github.com/Agents365-ai/thesis-reviewer) <br>
- [Agent Skills Format](https://agentskills.io) <br>
- [Universal Review Checklist](checklist.md) <br>
- [Review Report Template](output-template.md) <br>
- [Discipline-Specific Review Modules](disciplines/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Simplified Chinese Markdown review reports, including converted thesis Markdown, draft review reports, and final review reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires markitdown MCP for .docx conversion; review reports are saved beside the original thesis file.] <br>

## Skill Version(s): <br>
3.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
