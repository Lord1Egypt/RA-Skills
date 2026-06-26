## Description: <br>
Create vertical scarcity-mystery shorts with option teases, a confirmed final reveal, timed English captions, and WeryAI video generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zoucdr](https://clawhub.ai/user/zoucdr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to plan and run short-form WeryAI video generation for scarcity-mystery hooks. The agent expands a thesis-tease-reveal structure into timed captions, confirms the final reveal, and executes or proposes the Node.js video CLI flow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends prompts and selected image inputs to WeryAI using a paid API key. <br>
Mitigation: Use an isolated or short-lived WERYAI_API_KEY where possible, confirm prompts and image inputs before generation, and avoid including secrets or sensitive content. <br>
Risk: Local image paths may be read and uploaded by the helper script when used instead of public HTTPS image URLs. <br>
Mitigation: Prefer public HTTPS image URLs; use local paths only after reviewing the exact file and explicitly approving upload to WeryAI. <br>
Risk: The generated scarcity hook is creative short-form content and is not financial, therapeutic, or other professional advice. <br>
Mitigation: Review the final reveal, captions, and framing before publishing, especially when the topic could be interpreted as advice. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zoucdr/scarcest-not-money-video-gen) <br>
- [Publisher profile](https://clawhub.ai/user/zoucdr) <br>
- [WeryAI video CLI reference](resources/WERYAI_VIDEO_API.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with a video link, expanded prompt text, and inline JSON or shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WERYAI_API_KEY, Node.js 18+, paid network access to WeryAI, a non-empty model, and public HTTPS image URLs unless local upload is explicitly reviewed and approved.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
