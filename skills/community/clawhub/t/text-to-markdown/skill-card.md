## Description: <br>
Preprocesses plain text by inserting line breaks and splitting long paragraphs so an AI or LLM can produce better structured Markdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cizixiu](https://clawhub.ai/user/cizixiu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, writers, and knowledge workers use this skill to turn unstructured plain text, including long exported notes, into cleaner input for Markdown generation while preserving the original wording. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local text processing may expose sensitive document contents to any agent or process that handles the input. <br>
Mitigation: Run it only on files intended for processing and review the script first when inputs contain sensitive documents. <br>
Risk: Formatting changes may imply structure that the source text did not explicitly provide. <br>
Mitigation: Review the preprocessed output before using it as the basis for final Markdown. <br>


## Reference(s): <br>
- [Text to Markdown on ClawHub](https://clawhub.ai/cizixiu/text-to-markdown) <br>
- [Conversion Examples](references/examples.md) <br>
- [Markdown Format Reference](references/markdown-spec.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Plain text or Markdown, with optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preserves source wording while adjusting structure and line breaks.] <br>

## Skill Version(s): <br>
1.0.3 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
