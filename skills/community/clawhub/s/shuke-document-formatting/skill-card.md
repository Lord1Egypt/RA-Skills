## Description: <br>
Formats Word documents to Shuke company document-printing standards and generates PDFs using specified Chinese fonts, margins, grid, and line spacing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[an0027](https://clawhub.ai/user/an0027) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document operators use this skill to format Chinese Word documents to Shuke document-printing standards, install or verify required fonts, generate PDFs, and batch-convert document folders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The font installer can make persistent system font changes and may require sudo. <br>
Mitigation: Review the installer before use, run it only when Shuke fonts are needed, and prefer a controlled environment or explicit font source directory. <br>
Risk: PDF conversion can create local debug HTML and report files that may contain document content. <br>
Mitigation: Use narrow input and output folders, avoid confidential inputs unless appropriate, and delete generated *_debug.html files and batch reports after review. <br>
Risk: Formatting and PDF generation modify or create document files and depend on locally available fonts and tools. <br>
Mitigation: Keep original documents, test with a single file before batch conversion, and verify installed fonts and generated PDFs before distribution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/an0027/shuke-document-formatting) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with Python commands; generated artifacts are DOCX, PDF, font verification text, batch reports, and optional debug HTML files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are local files and console status messages; results depend on Python dependencies, Pandoc or PDF tooling, and locally installed fonts.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact config files report 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
