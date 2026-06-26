## Description: <br>
Extractive AI text summarizer. Automatically extracts the most important sentences from any text using a hybrid TextRank + TF-IDF algorithm. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to condense articles, reports, papers, notes, emails, or pasted prose into a shorter extractive summary. It supports short, medium, and long length presets plus bullet or paragraph output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pasted text and input files may contain sensitive content, and selected source sentences can be printed in the summary output. <br>
Mitigation: Treat all input text and file paths as sensitive; avoid using confidential material unless local handling is acceptable. <br>
Risk: Extractive summaries can omit context even when they quote source sentences exactly. <br>
Mitigation: Review summaries against the original document when accuracy, completeness, or decision-making impact matters. <br>
Risk: The summarizer is optimized for English prose and is not designed for code, tables, structured data, multilingual content, or cross-document summarization. <br>
Mitigation: Use it for single-document English prose, and choose a different workflow for structured, multilingual, or multi-document material. <br>


## Reference(s): <br>
- [Extractive Summarization Algorithm Reference](references/algorithms.md) <br>
- [ClawHub skill page](https://clawhub.ai/openlark/text-summarizer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Plain text or Markdown-style bullets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Extractive summaries use exact source sentences; length presets are short, medium, and long, with bullet or paragraph formats.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
