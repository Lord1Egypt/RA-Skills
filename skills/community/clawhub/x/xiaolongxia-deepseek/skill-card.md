## Description: <br>
小龙虾-DeepSeek版 is a DeepSeek API-backed coding assistant for code generation, review, debugging, optimization, refactoring, and explanation with multi-turn conversation memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pengpengliu1212-art](https://clawhub.ai/user/pengpengliu1212-art) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to ask coding questions, generate or revise code, review snippets, debug errors, optimize implementations, and continue prior coding discussions through saved conversation context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and saved conversation context are sent to DeepSeek and retained locally between runs. <br>
Mitigation: Avoid API keys, proprietary code, regulated data, and incident details; clear conversation history before sensitive work. <br>
Risk: Broad coding trigger phrases may route ordinary development requests through this skill. <br>
Mitigation: Invoke it deliberately and review generated code, commands, and recommendations before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pengpengliu1212-art/xiaolongxia-deepseek) <br>
- [DeepSeek API endpoint](https://api.deepseek.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with code blocks and command-line status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist and reuse conversation history across invocations; DeepSeek API responses are capped at 4096 tokens by the artifact configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact/skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
