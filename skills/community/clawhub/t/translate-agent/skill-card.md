## Description: <br>
Stateless translation and summarization skill that returns raw JSON for translate, summarize, translate_and_summarize, heartbeat, and error responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AnhducNA](https://clawhub.ai/user/AnhducNA) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to standardize translation and summarization requests into deterministic JSON outputs. It is suited for workflows that need language detection, Vietnamese default translation, summary key points, and consistent error responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad routing language may cause ordinary translation-like messages to be handled by this skill unexpectedly. <br>
Mitigation: Review invocation rules before deployment and route only requests that require the skill's strict JSON translation or summarization format. <br>
Risk: Plain text defaults to Vietnamese translation when no target language is provided. <br>
Mitigation: Provide an explicit target_lang value whenever the desired output language is not Vietnamese. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/AnhducNA/translate-agent) <br>
- [Publisher Profile](https://clawhub.ai/user/AnhducNA) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [Raw JSON object] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs only JSON without markdown, explanations, preambles, or code fences.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
