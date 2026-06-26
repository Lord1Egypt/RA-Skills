## Description: <br>
易经占卜大师 calls the Li Xiaowen API to cast and interpret I Ching/Yijing hexagrams, supporting coin casting, Dayan casting, user-provided hexagrams, Markdown rendering, and terminal ASCII rendering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liquanyu123](https://clawhub.ai/user/liquanyu123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to request I Ching/Yijing divination-style readings for a stated question or situation. The skill sends the user's prompt to the configured external service and returns a Markdown or terminal-friendly interpretation with hexagram details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger patterns could route ordinary user messages to the external API. <br>
Mitigation: Review and narrow the trigger patterns before enabling automatic activation. <br>
Risk: User prompts are sent to wenmutang.top for processing. <br>
Mitigation: Install only if external processing is acceptable and avoid sharing sensitive personal details. <br>
Risk: The skill requires an API key. <br>
Mitigation: Store the API key outside the skill file when the agent supports external secret storage. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liquanyu123/yijing-suangua) <br>
- [Publisher profile](https://clawhub.ai/user/liquanyu123) <br>
- [External service website](https://wenmutang.top) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with optional terminal ASCII hexagram and rating blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires API_KEY and RENDER_STYLE configuration; prompts are sent to an external API service.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
