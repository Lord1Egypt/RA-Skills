## Description: <br>
Adaptive multi-model AI roundtable that runs configurable debate, critique, validation, and synthesis workflows across Claude, GPT, Gemini, and Grok providers, with Claude-only fallback and local result persistence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JimmyClanker](https://clawhub.ai/user/JimmyClanker) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, product teams, and operators use this skill to convene multiple AI models for structured debate, red-team review, build planning, option voting, and synthesized recommendations on a submitted topic. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted topics, context, critiques, and summaries may be sent to web search, multiple model providers, and possibly Discord. <br>
Mitigation: Use the skill only with data approved for those destinations, configure provider access deliberately, and avoid secrets, regulated data, or proprietary strategy. <br>
Risk: Roundtable outputs may be retained or reused through local memory and persistent thread sessions. <br>
Mitigation: Review the configured memory directory and thread behavior before use, and disable persistence or remove saved records when retention is not appropriate. <br>
Risk: Auto-triggered Discord channel use could process messages without an explicit command. <br>
Mitigation: Restrict auto-trigger configuration to dedicated channels and prefer explicit `roundtable` commands where message scope needs tight control. <br>


## Reference(s): <br>
- [Roundtable README](artifact/README.md) <br>
- [Roundtable skill definition](artifact/SKILL.md) <br>
- [Panel configuration](artifact/panels.json) <br>
- [Final output schema](artifact/schemas/final-output.schema.json) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [ClawHub skill page](https://clawhub.ai/JimmyClanker/roundtable-adaptive) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Configuration, Guidance] <br>
**Output Format:** [Structured Markdown synthesis with optional JSON run records and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May post results to a configured Discord channel or thread and persist run records under the workspace memory directory.] <br>

## Skill Version(s): <br>
2.9.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
