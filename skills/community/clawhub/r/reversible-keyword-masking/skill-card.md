## Description: <br>
Reversible Keyword Masking (RKM) locally masks sensitive document keywords with stable placeholders before AI editing, then verifies and restores them from an encrypted local mapping. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fuetsui](https://clawhub.ai/user/fuetsui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, writers, legal operations staff, and business users can use this skill to mask configured sensitive terms before sending documents to an AI model for editing, rewriting, translating, summarizing, polishing, or restructuring. It is most useful when placeholders must be verified and restored locally after AI editing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local CLI reads and writes documents in its working directory. <br>
Mitigation: Install and run it only in directories where local document processing is acceptable, and review input, output, and mapping paths before execution. <br>
Risk: Mapping files, password files, and RKM_KEY can reveal or unlock sensitive originals. <br>
Mitigation: Keep mapping files, password files, and RKM_KEY private, exclude them from Git, and avoid sharing decrypted mapping data with remote models. <br>
Risk: Legacy .doc conversion relies on Microsoft Word or LibreOffice parsers with their own attack surface. <br>
Mitigation: Prefer .txt, .md, or .docx for untrusted documents, or run legacy .doc conversion in a sandboxed or offline environment. <br>
Risk: The skill masks explicit keywords and matched patterns, not indirect context, business logic, document structure, or writing style. <br>
Mitigation: Review masked documents for remaining contextual clues, add missing terms or regex patterns, and avoid treating masking as complete anonymization. <br>


## Reference(s): <br>
- [Skill Instructions](SKILL.md) <br>
- [README](README.md) <br>
- [RKM Keyword Configuration](references/keyword-config.md) <br>
- [Custom Keyword Template](references/custom-keywords.txt) <br>
- [Fictional Sample Workflow](examples/README.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/fuetsui/skills/reversible-keyword-masking) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files, JSON] <br>
**Output Format:** [Markdown instructions with shell commands; the CLI can produce masked/restored document files, encrypted mapping files, and JSON reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local filesystem output; mapping files are encrypted, and scan/verification reports omit raw sensitive values.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata, manifest.yaml, README.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
