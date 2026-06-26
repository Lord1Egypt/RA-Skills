## Description: <br>
Text generation and chat completion on Volcengine ARK. Use when users need long-form writing, summarization, extraction, rewriting, Q&A, or prompt optimization with ARK text models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to prepare ARK chat completion requests, run text generation workflows, and return generated content with the key parameters used. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Volcengine ARK API key and can expose credentials if commands or logs are shared carelessly. <br>
Mitigation: Keep ARK_API_KEY private, scope it appropriately, and avoid pasting secrets into prompts, command output, or shared transcripts. <br>
Risk: Prompts sent to ARK may include sensitive personal, proprietary, or regulated content. <br>
Mitigation: Send sensitive data only when it is acceptable under the user's Volcengine account terms and organizational data-handling rules. <br>


## Reference(s): <br>
- [Sources](references/sources.md) <br>
- [Volcengine ARK Chat Completions API endpoint](https://ark.cn-beijing.volces.com/api/v3/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with generated text, parameter notes, and optional bash request templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses ARK_API_KEY and a caller-provided endpoint ID, region, and generation parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
