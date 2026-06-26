## Description: <br>
Extracts structured weekly menu content, including breakfast, lunch, and snacks by day, from a cafeteria menu image using a vision-language model via OpenRouter. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ihainan](https://clawhub.ai/user/ihainan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to extract a weekly cafeteria menu from a PNG or JPEG image into organized day-by-day menu text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The selected cafeteria menu image is sent to OpenRouter for processing. <br>
Mitigation: Use only images you are comfortable sharing with OpenRouter, and avoid images containing people, badges, private notices, or unrelated sensitive content. <br>
Risk: The extraction script may contain a syntax error in its prompt string. <br>
Mitigation: Review and fix the script before relying on it in an agent workflow. <br>
Risk: The skill requires a user-provided OpenRouter API key. <br>
Mitigation: Configure MENU_OPENROUTER_API_KEY only in the execution environment and do not include the key in prompts, images, logs, or shared files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ihainan/zgcai-weekly-restaurant-menu-skill) <br>
- [Publisher profile](https://clawhub.ai/user/ihainan) <br>
- [OpenRouter chat completions API](https://openrouter.ai/api/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration] <br>
**Output Format:** [Structured Markdown menu output with optional command-line usage and environment setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MENU_OPENROUTER_API_KEY and a user-selected PNG or JPEG menu image.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
