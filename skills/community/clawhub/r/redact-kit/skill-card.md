## Description: <br>
Scan your data before sending it to AI. Detect and redact PII, secrets, and sensitive info. Reversible, local, zero network calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[theshadowrose](https://clawhub.ai/user/theshadowrose) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and other external users use RedactKit to scan text, code, logs, and documents for PII, secrets, and sensitive data before sharing them with AI tools or collaborators. Users can optionally keep local mapping files to restore redacted values after processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reversible redaction can leave original sensitive values in plaintext mapping files, including in workflows where users may expect report mode to be read-only. <br>
Mitigation: Use non-reversible redaction unless restoration is required; keep mapping files out of repositories and cloud sync, restrict or encrypt them, and avoid combining --report with --mapping. <br>
Risk: Regex-based detection can miss obfuscated or non-standard sensitive data and can also flag false positives. <br>
Mitigation: Review report-mode output before batch redaction, add custom patterns or exclusions for local data formats, and validate outputs before sharing. <br>
Risk: Batch operations can process unintended files or create mapping files in broad directory trees. <br>
Mitigation: Use narrow input and output directories, set explicit extensions, and review generated outputs and mappings before reuse. <br>
Risk: The tool does not provide compliance certification for regulated data. <br>
Mitigation: Treat it as one control in a broader compliance process and have regulated workflows reviewed by qualified security or legal professionals. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/theshadowrose/redact-kit) <br>
- [README.md](artifact/README.md) <br>
- [LIMITATIONS.md](artifact/LIMITATIONS.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python and shell snippets; runtime tools produce redacted text files and JSON mapping files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local regex-based processing with optional reversible mappings that can contain original sensitive values.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
