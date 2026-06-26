## Description: <br>
Fix garbled text in PDF/SVG vector graphics for final editing in AI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EC-cyber258](https://clawhub.ai/user/EC-cyber258) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document workflow users use this skill to inspect PDF or SVG vector files, detect garbled text caused by encoding or font issues, and prepare repair suggestions, editable JSON, or local file-processing commands for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local document processing can read source PDF/SVG files and write output files, reports, or JSON exports. <br>
Mitigation: Run the tool only on copies of intended documents, review input and output paths before execution, and keep generated files inside the expected workspace. <br>
Risk: Repair suggestions, logs, and JSON exports may contain private source-document text or inaccurate replacements. <br>
Mitigation: Treat exports and logs as sensitive, review suggested fixes manually, and avoid relying on repaired text without human confirmation. <br>
Risk: The skill depends on local Python packages for PDF/SVG parsing and text processing. <br>
Mitigation: Install dependencies deliberately, preferably pinned and from trusted package names, before running the commands. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/EC-cyber258/vector-text-fixer) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, JSON, Code] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON export structures] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local PDF/SVG processing instructions, repair summaries, and editable JSON maps for manual review.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
