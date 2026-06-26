## Description: <br>
Auto-annotate cell clusters from single-cell RNA data using marker genes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External researchers and bioinformatics developers use this skill to annotate post-clustering single-cell RNA clusters from marker genes, with explicit assumptions, confidence levels, alternatives, risks, and next checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local Python execution and an unpinned pandas dependency can create environment drift or dependency exposure. <br>
Mitigation: Install in a virtual environment, review the script before use, and pin or audit pandas for the deployment environment. <br>
Risk: Marker-based annotation can produce incomplete or misleading labels when inputs lack tissue, species, or sufficient marker support. <br>
Mitigation: Use only clear scRNA marker-based cluster annotation inputs, document assumptions, and have a qualified reviewer validate predictions and alternatives. <br>
Risk: Local input and output files may contain research data that should remain scoped to the workspace. <br>
Mitigation: Validate file paths, run in a sandboxed workspace, and avoid including sensitive data in final outputs unless explicitly required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aipoch-ai/scrna-cell-type-annotator) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with structured sections and optional shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include cell type predictions, marker gene support, confidence scores, alternative suggestions, assumptions, risks, and next checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
