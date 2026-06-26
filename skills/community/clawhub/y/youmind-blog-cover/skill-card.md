## Description: <br>
Generate blog cover images optimized for 16:9 headers with clean, text-friendly layouts powered by multi-model AI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dophinl](https://clawhub.ai/user/dophinl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, content creators, and developers use this skill to turn an article title, topic, or URL into a professional 16:9 blog cover image through YouMind. It is intended for agent-assisted image generation workflows that return board links and generated image URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests broader local command authority than needed, including Node.js script execution and global CLI installation. <br>
Mitigation: Review the allowed commands before deployment and narrow or justify Node.js and install permissions in managed environments. <br>
Risk: Remote image generation requires a YouMind API key and stores generated images on a YouMind board. <br>
Mitigation: Configure the API key outside chat history, avoid exposing secrets, and tell users where generated images are stored. <br>
Risk: Ambiguous image-related requests may activate the skill unexpectedly. <br>
Mitigation: Confirm the user's article topic or intent before invoking remote generation when the request is unclear. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dophinl/youmind-blog-cover) <br>
- [YouMind CLI package](https://www.npmjs.com/package/@youmind-ai/cli) <br>
- [YouMind](https://youmind.com?utm_source=youmind-blog-cover) <br>
- [YouMind skills gallery](https://youmind.com/skills?utm_source=youmind-blog-cover) <br>
- [Setup guide](references/setup.md) <br>
- [Error handling](references/error-handling.md) <br>
- [Long-running tasks](references/long-running-tasks.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, status updates, board links, and generated image URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the YouMind CLI and API for remote image generation, polls long-running work, and saves generated images to the user's YouMind board.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
