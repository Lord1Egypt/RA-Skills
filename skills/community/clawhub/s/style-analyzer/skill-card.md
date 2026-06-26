## Description: <br>
Style Analyzer analyzes writing-style characteristics and generates a Voice Profile YAML file for capturing author style, creating voice profiles, and analyzing sentence, vocabulary, rhythm, and sentiment features. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuzhihui886](https://clawhub.ai/user/yuzhihui886) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and writers use this skill to analyze reference text and produce a Voice Profile configuration that can guide consistent style in fiction or prompt-building workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The LLM analysis mode can send selected input text to DashScope when DASHSCOPE_API_KEY is configured. <br>
Mitigation: Use scripts/analyze_style.py for local-only analysis, and run scripts/analyze_style_llm.py only when external processing of the selected text is acceptable. <br>
Risk: Confidential drafts, business documents, or personal data may be exposed if they are analyzed through the LLM mode. <br>
Mitigation: Avoid submitting sensitive text to the LLM mode unless that external processing has been reviewed and approved. <br>
Risk: Unpinned Python dependencies can reduce repeatability in sensitive environments. <br>
Mitigation: Pin and review dependencies before installing or running the skill in a controlled environment. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown instructions with shell commands; generated analysis is saved as YAML.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The local analyzer can write sentence, vocabulary, rhythm, and voice profile fields; the LLM analyzer writes a voice profile and analysis notes.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
