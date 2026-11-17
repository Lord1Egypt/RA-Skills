## Description:

Reversible Keyword Masking (RKM) helps agents guide users through local masking of sensitive document keywords with stable placeholders, encrypted local mappings, verification, repair, and restoration before or after AI editing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fuetsui](https://clawhub.ai/user/fuetsui)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill when documents need editing, rewriting, translation, summarization, polishing, or restructuring while explicit sensitive keywords should stay out of the model context. It is especially suited to workflows that can run a local CLI to mask, verify, repair, and restore placeholders around AI-edited content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Legacy Word document handling can invoke local Office or LibreOffice on user-selected files.

Mitigation: Avoid untrusted legacy .doc files, or convert and inspect them in a sandbox or isolated environment before using the skill.

Risk: Mapping files, password files, RKM_KEY values, or decrypted mappings could expose the sensitive keywords the skill is intended to protect.

Mitigation: Keep mapping files, password files, environment values, and decrypted mapping data local and out of chats, logs, and Git.

Risk: Keyword masking protects explicit terms and configured pattern matches, but not indirect context, business logic, document structure, or background clues.

Mitigation: Review masked documents for residual contextual disclosure before sending them to an AI model, and add explicit keywords or patterns when needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fuetsui/skills/reversible-keyword-masking)
- [Keyword Configuration](references/keyword-config.md)
- [Custom Keyword Template](references/custom-keywords.txt)
- [Example Workflow](examples/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with command examples, configuration snippets, and local file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local masked documents, encrypted mapping files, verification reports, repaired masked files, and restored documents when the user runs the bundled CLI.]

## Skill Version(s):

1.0.1 (source: server release metadata and manifest.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
