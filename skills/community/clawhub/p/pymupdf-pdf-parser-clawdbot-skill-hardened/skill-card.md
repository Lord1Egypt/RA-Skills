## Description: <br>
Fast local PDF parsing with PyMuPDF (fitz) for Markdown/JSON outputs and optional images/tables, intended for single-PDF parsing with per-document output folders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to extract local PDF content quickly into Markdown or JSON, with optional image extraction and rough table output. It is best suited for speed-focused text extraction where complex layout preservation is not required. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Extracted PDF content is saved as cleartext local files. <br>
Mitigation: Run the parser only on PDFs intended for extraction and choose an output directory appropriate for the sensitivity of the content. <br>
Risk: Unsafe shell command construction can mishandle PDF paths. <br>
Mitigation: Quote file paths safely when running commands and avoid passing unvalidated shell metacharacters. <br>
Risk: Batch or recursive parsing can expose a large document store as local cleartext output. <br>
Mitigation: Confirm before batch processing directories or sensitive document stores. <br>
Risk: Installing parser dependencies from an untrusted source can introduce supply-chain risk. <br>
Mitigation: Install PyMuPDF only from a trusted package source. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/snazar-faberlens/pymupdf-pdf-parser-clawdbot-skill-hardened) <br>
- [PyMuPDF documentation](https://pymupdf.readthedocs.io/) <br>
- [PyMuPDF Notes](references/pymupdf-notes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands; the parser writes local Markdown, JSON, image, and table files when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates per-document local output directories and can optionally extract embedded images and simple line-based table JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
