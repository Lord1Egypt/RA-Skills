## Description: <br>
Universal Translate translates text, files, and conversations between languages while auto-detecting the source language and preserving formatting, tone, and technical terms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vanthienha199](https://clawhub.ai/user/vanthienha199) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to translate messages, documents, and multilingual conversations while preserving formatting and technical context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad translation prompts or omitted target languages can produce unintended default translations. <br>
Mitigation: Ask the user for the target language when it is unclear and show the detected source and target language pair. <br>
Risk: File translation can cause the agent to read and write files the user did not intend to process. <br>
Mitigation: Only translate explicitly requested files and save translated copies with language-code suffixes. <br>
Risk: Interpreter mode can continue longer than intended during a conversation. <br>
Mitigation: Continue interpreter mode only until the user says to stop translating. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Files, Guidance] <br>
**Output Format:** [Markdown text, optional translated files, and summary tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preserves formatting and code blocks; translated files are saved with language-code suffixes when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
