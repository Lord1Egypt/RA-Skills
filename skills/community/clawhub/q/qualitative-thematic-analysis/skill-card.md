## Description: <br>
基于 Braun & Clarke 六阶段法，对本地质性资料（访谈、观察、文本）进行系统性主题归纳、编码及报告生成。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yipng05-max](https://clawhub.ai/user/yipng05-max) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, analysts, and teams use this skill to analyze local qualitative materials such as interview transcripts, observation notes, focus group records, and text corpora. It guides the agent through familiarization, initial coding, theme development, theme review, naming, and report generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Qualitative research files may contain participant identifiers or sensitive interview content. <br>
Mitigation: Use a dedicated folder, remove unrelated files, anonymize participant details where possible, confirm consent for AI-assisted analysis, and store generated outputs as sensitive research data. <br>
Risk: Outputs may include excerpts from source materials in coding tables or reports. <br>
Mitigation: Review exported coding tables and reports before sharing, and redact or pseudonymize direct quotations when needed. <br>
Risk: The artifact notes earlier workflow risks around shallow analysis, skipped intermediate coding stages, and missing saturation checks. <br>
Mitigation: Require full text extraction, explicit initial codes, theme review, representative quotes with source locations, and saturation checks before relying on findings. <br>


## Reference(s): <br>
- [Thematic Analysis Method](references/thematic-analysis-method.md) <br>
- [Coding Guide](references/coding-guide.md) <br>
- [Ethics Note](references/ethics-note.md) <br>
- [ClawHub skill page](https://clawhub.ai/yipng05-max/qualitative-thematic-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional Excel coding tables and DOCX reports generated from JSON inputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads user-specified local TXT, DOCX, and PDF files; generated outputs should be treated as sensitive research data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
