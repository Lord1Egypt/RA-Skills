## Description: <br>
Yinian Zi Wei Dou Shu provides AI-assisted chart generation and cultural-reference readings for Zi Wei Dou Shu using Sanhe, Feixing, and Zhan Yan analysis styles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vincent-vstudios](https://clawhub.ai/user/vincent-vstudios) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to collect birth details, generate Zi Wei Dou Shu charts, and produce cultural-reference readings across palace, star, four-transformation, and timing views. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Birth details and generated chart content can be sent to a remote LLM provider when AI readings are used. <br>
Mitigation: Tell users before AI readings are requested, avoid submitting data they do not want transmitted externally, and use local chart-only commands when external transmission is not acceptable. <br>
Risk: The skill can automatically use local API credentials for DeepSeek or OpenAI-compatible providers. <br>
Mitigation: Use a dedicated DeepSeek key with limited blast radius instead of a broad shared key, and keep credentials out of prompts, logs, and public configuration. <br>
Risk: The included FastAPI service is risky if exposed publicly with permissive CORS and prompt-facing fields. <br>
Mitigation: Do not expose the API publicly without tightening CORS, removing unnecessary prompt fields, and adding normal service controls such as authentication, logging review, and rate limits. <br>
Risk: Astrology readings may be mistaken for medical, legal, financial, relationship, or other life-decision advice. <br>
Mitigation: Keep the skill's cultural-reference disclaimer, avoid absolute predictions, and direct users to qualified professionals for high-stakes decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vincent-vstudios/yinian-zwds) <br>
- [Four Transformations reference](references/mutagen.md) <br>
- [Twelve Palaces reference](references/palaces.md) <br>
- [Sanhe, Feixing, and Zhan Yan reference](references/sanhe.md) <br>
- [Stars reference](references/stars.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON or API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use local chart generation or remote LLM-backed readings when configured with API credentials.] <br>

## Skill Version(s): <br>
2.1.0 (source: frontmatter and release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
