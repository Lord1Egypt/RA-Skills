## Description: <br>
Converts a local project contract .docx into a formatted Word requirements specification with extracted project details and generated architecture diagrams. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lan2898408767](https://clawhub.ai/user/lan2898408767) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users or document automation teams use this skill to turn Chinese project contract files into standardized requirements specification documents. It reads a desktop contract file, generates a system architecture diagram, and writes a formatted .docx output for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can select the wrong Desktop contract file when an explicit input path is not provided. <br>
Mitigation: Run it on a copy of the intended contract, confirm the exact input file before execution, and require explicit file paths before operational use. <br>
Risk: The generated document may contain hard-coded or incomplete contract details while appearing authoritative. <br>
Mitigation: Manually verify contract number, parties, requirements, and generated diagrams before relying on the Word document; remove hard-coded contract data in the implementation. <br>
Risk: Dependencies and behavior are not fully disclosed or pinned in the artifact. <br>
Mitigation: Review and pin required dependencies, then confirm the implementation matches the stated workflow before installation. <br>


## Reference(s): <br>
- [需求规格说明书格式规范](references/format_spec.md) <br>
- [ClawHub release page](https://clawhub.ai/lan2898408767/shucheng-contract-to-spec) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [Word document (.docx) with generated HTML/PNG intermediates and console status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes the final document to the user's Desktop using the pattern {project name} 需求规格说明书_v6.0.docx.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
