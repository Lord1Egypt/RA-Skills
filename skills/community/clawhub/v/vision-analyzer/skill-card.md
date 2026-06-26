## Description: <br>
Analyze images using Ollama Cloud's Kimi K2.5 vision capabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kawummuwe-stack](https://clawhub.ai/user/kawummuwe-stack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to describe, inspect, and ask targeted questions about local images, screenshots, photos, charts, diagrams, and UI captures through Ollama Cloud vision analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Images and prompts are sent to Ollama Cloud for processing, which may expose secrets, personal information, customer data, or proprietary material contained in the selected image. <br>
Mitigation: Use the skill only with images that are acceptable to share with Ollama Cloud, and avoid screenshots, documents, photos, or UI captures containing sensitive data unless that sharing has been approved. <br>
Risk: The skill requires an Ollama API key in the OLLAMA_API_KEY environment variable. <br>
Mitigation: Store the key outside prompts and shared artifacts, pass it through the local environment, and rotate it if it may have been exposed. <br>


## Reference(s): <br>
- [Vision Analyzer on ClawHub](https://clawhub.ai/kawummuwe-stack/vision-analyzer) <br>
- [Publisher profile](https://clawhub.ai/user/kawummuwe-stack) <br>
- [Ollama API settings](https://ollama.com/settings) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text or Markdown with command-line examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OLLAMA_API_KEY and sends the selected image plus prompt to Ollama Cloud for analysis.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
