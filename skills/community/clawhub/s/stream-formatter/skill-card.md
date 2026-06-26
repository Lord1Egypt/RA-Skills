## Description: <br>
LLM streaming output formatter with auto buffer, format correction, sentence break optimization, markdown rendering, improve chat UX. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ayalili](https://clawhub.ai/user/Ayalili) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers building chat agents, chatbots, and real-time content generation flows use this skill to buffer streamed LLM chunks, emit complete sentence-oriented text, reduce duplicate output, and repair common Markdown formatting issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill keeps recent streamed text in memory while buffering and deduplicating output. <br>
Mitigation: Call init before starting a new stream and reset after use or when switching conversations. <br>
Risk: The skill loads a pinned Zod dependency from deno.land. <br>
Mitigation: Review the pinned dependency and allow network access to deno.land only when that dependency source is acceptable for the deployment environment. <br>


## Reference(s): <br>
- [stream-formatter on ClawHub](https://clawhub.ai/Ayalili/stream-formatter) <br>
- [Pinned Zod dependency](https://deno.land/x/zod@v3.22.4/mod.ts) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [JSON object containing formatted streamed text and buffer status] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes init, process, and reset actions; stores recent streamed text in memory until init or reset is called.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
