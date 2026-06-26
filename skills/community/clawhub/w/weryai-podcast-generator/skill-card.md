## Description: <br>
Generate, query, and deliver WeryAI podcasts through the official podcast generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weryai-developer](https://clawhub.ai/user/weryai-developer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to list WeryAI podcast speakers, submit podcast text generation, trigger audio generation, check task status, and deliver finished podcast audio links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a WeryAI API key and can spend paid WeryAI credits during podcast generation. <br>
Mitigation: Install only from a trusted publisher, keep WERYAI_API_KEY private, confirm query, speakers, language, and mode before paid runs, and use dry-run for request-shape checks. <br>
Risk: WERYAI_BASE_URL can redirect requests, including authenticated requests, to a different endpoint. <br>
Mitigation: Leave WERYAI_BASE_URL unset or pointed at the official WeryAI API host unless the alternate endpoint is intentionally trusted. <br>
Risk: The artifact includes extra vendored music helpers that are outside the documented podcast workflow. <br>
Mitigation: Use the documented podcast entrypoints only: speakers.js, submit-text.js, generate-audio.js, status.js, and wait.js. <br>
Risk: Podcast generation is asynchronous and may run for an extended period before audio is ready. <br>
Mitigation: Use the documented bounded wait flow, enforce the 30-minute maximum timeout, and return task status for later follow-up when completion is delayed. <br>


## Reference(s): <br>
- [Weryai Podcast Generator on ClawHub](https://clawhub.ai/weryai-developer/weryai-podcast-generator) <br>
- [weryai-developer ClawHub Profile](https://clawhub.ai/user/weryai-developer) <br>
- [Official Podcast API Summary](references/podcast-api.md) <br>
- [Get Podcast Speakers List](https://docs.weryai.com/api-reference/podcast-generation/get-podcast-speakers-list) <br>
- [Submit Podcast Text Generation Task](https://docs.weryai.com/api-reference/podcast-generation/submit-podcast-text-generation-task) <br>
- [Generate Podcast Audio](https://docs.weryai.com/api-reference/podcast-generation/generate-podcast-audio) <br>
- [Query Task Details](https://docs.weryai.com/api-reference/tasks/query-task-details) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with task summaries, speaker information, final audio links, and concise command-oriented guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js >=18 and WERYAI_API_KEY; real submit, audio, and wait runs may consume WeryAI credits.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
