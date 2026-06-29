## Description: <br>
Gugu Gaga analyzes pharmaceutical regulatory and guidance documents from PDF, DOCX, DOC, or TXT inputs and turns them into structured analysis reports for training presentations or study-sharing PDFs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gxpcode-hezhong](https://clawhub.ai/user/gxpcode-hezhong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Regulatory, quality, and pharmaceutical professionals use this skill to break down pharmaceutical regulations or guidance into element collection, characterization, key content, lifecycle diagrams, and red-yellow-green-blue compliance summaries. It helps create reviewable training decks or study PDFs from local source documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Packaged preview assets and conversion code may load third-party resources or otherwise behave more broadly than the document-analysis workflow suggests. <br>
Mitigation: Review generated HTML before conversion, block unexpected external network access in sensitive environments, and use local source documents only. <br>
Risk: Document conversion can expose local files or content to broader converter behavior if optional cloud or plugin features are enabled. <br>
Mitigation: Use only local PDF, DOC, DOCX, or TXT inputs and avoid enabling MarkItDown cloud or plugin flags unless separately reviewed. <br>


## Reference(s): <br>
- [Server-resolved GitHub repository](https://github.com/Gxpcode-hezhong/Regulatory-Guidance-Analysis-Tool) <br>
- [ClawHub skill page](https://clawhub.ai/gxpcode-hezhong/skills/regulatory-guidance-analysis-tool) <br>
- [Microsoft MarkItDown documentation](https://github.com/microsoft/markitdown) <br>
- [MarkItDown security considerations](https://github.com/microsoft/markitdown#security-considerations) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Files, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown analysis files, generated HTML previews, and final PPTX or PDF files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are selected by the user as either a training presentation PPTX or a study-sharing PDF.] <br>

## Skill Version(s): <br>
0.1.1 (source: ClawHub release metadata; artifact frontmatter reports 2.5.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
