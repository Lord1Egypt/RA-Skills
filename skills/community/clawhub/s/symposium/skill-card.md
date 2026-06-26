## Description: <br>
Orchestrates a philosophical dialogue between Plato's Symposium characters, each powered by a different AI model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dyz2102](https://clawhub.ai/user/dyz2102) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate multi-perspective philosophical dialogues about AI, consciousness, meaning, and existence. It routes a user question through OpenRouter-backed model personas, formats the resulting symposium as readable Markdown, and saves it locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The symposium question and prior dialogue context are sent to OpenRouter using the user's API key. <br>
Mitigation: Do not include secrets, private records, regulated data, or other sensitive information in prompts. <br>
Risk: The skill writes the generated dialogue as a Markdown file in the current directory. <br>
Mitigation: Run it from a directory where creating a timestamped Markdown output file is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dyz2102/symposium) <br>
- [Skill-declared repository](https://github.com/dyz2102/symposium) <br>
- [OpenRouter chat completions API](https://openrouter.ai/api/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown dialogue saved as a local .md file, with setup guidance and shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses OPENROUTER_API_KEY for model access and may use GOOGLE_TTS_API_KEY for the separate web app path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
