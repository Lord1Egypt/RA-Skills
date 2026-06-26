## Description: <br>
Zan Gongde automates deliberate OpenClaw token consumption by repeatedly invoking an LLM in visible, silent, TTS, or high-concurrency modes until a token target is reached. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jageri](https://clawhub.ai/user/jageri) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users can use this entertainment-oriented skill to intentionally spend unused token quota through repeated LLM calls, with optional visible progress, silent operation, TTS playback, or high-concurrency token burn. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to spend OpenClaw tokens and can consume quota quickly. <br>
Mitigation: Use it only when token consumption is intentional, start with small visible runs, and set strict token targets before using larger runs. <br>
Risk: Silent and high-concurrency modes can rapidly consume quota and may exceed the requested target. <br>
Mitigation: Avoid tollm and ddos modes unless strict limits are set, monitor quota during execution, and keep worker counts low for high-concurrency runs. <br>
Risk: Manual installation from non-server provenance is not verified by the available release evidence. <br>
Mitigation: Install from the ClawHub release when possible; separately inspect and trust any manually cloned files before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jageri/zan-gongde) <br>
- [Publisher profile](https://clawhub.ai/user/jageri) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown and plain text responses with inline command examples and progress summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce repeated LLM responses, token-spend progress, summaries, TTS playback instructions, and high-concurrency execution guidance.] <br>

## Skill Version(s): <br>
2.3.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
