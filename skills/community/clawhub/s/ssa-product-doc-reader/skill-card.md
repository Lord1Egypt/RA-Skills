## Description: <br>
Product Doc Reader extracts structured product specifications, BOMs, model numbers, packaging codes, test requirements, and drawing metadata from product engineering drawing PDFs using text-first parsing with optional vision fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cjboy007](https://clawhub.ai/user/cjboy007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations users can use this skill to convert product engineering drawing PDFs into structured JSON and Markdown records for product databases, knowledge bases, BOM review, and batch document processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Product drawing images may be sent to third-party AI APIs during vision analysis. <br>
Mitigation: Use --text-only for confidential drawings unless third-party upload is approved. <br>
Risk: A hard-coded API credential is present in the artifact. <br>
Mitigation: Review and replace credential handling before use; provide user-controlled API credentials when vision analysis is required. <br>
Risk: Batch cleanup paths can remove temporary directories. <br>
Mitigation: Run batch workflows only with WORKSPACE and --temp-dir set to a safe disposable directory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cjboy007/ssa-product-doc-reader) <br>
- [Publisher profile](https://clawhub.ai/user/cjboy007) <br>
- [Artifact skill documentation](artifact/SKILL.md) <br>
- [Development summary](artifact/DEVELOPMENT_SUMMARY.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Markdown, Shell commands, Guidance] <br>
**Output Format:** [JSON and Markdown extraction reports, with optional stdout JSON from command-line scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes PDF input files and can write report files to a selected output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
