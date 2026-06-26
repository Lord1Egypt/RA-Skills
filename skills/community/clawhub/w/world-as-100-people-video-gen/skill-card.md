## Description: <br>
Create ‘world as 100 people’ verticals: shrink hook, stat morphs, punchline, timed English captions and motion graphics (WeryAI). Use for infographic TikToks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zoucdr](https://clawhub.ai/user/zoucdr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, marketers, educators, and agent operators use this skill to prepare and submit short vertical infographic videos built around the 'world as 100 people' metaphor, with timed English captions, icon motion, and a final punchline stat. The user is responsible for the factual claims behind any demographic or statistical statements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a paid WeryAI API key and sends prompts, and optionally selected images, to WeryAI. <br>
Mitigation: Keep WERYAI_API_KEY out of shared files and logs, use an isolated or short-lived environment when appropriate, and confirm the user is comfortable sending the prompt and image inputs to WeryAI. <br>
Risk: Local image paths can be read and uploaded before generation when used instead of public HTTPS URLs. <br>
Mitigation: Prefer public HTTPS image URLs; use local paths only after reviewing the behavior and obtaining explicit consent to read and upload those files. <br>
Risk: Generated demographic videos may imply factual claims that the skill does not independently verify. <br>
Mitigation: Ask the user to provide or approve the stats, keep captions short and clear, and treat the output as illustrative unless claims are separately sourced. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zoucdr/world-as-100-people-video-gen) <br>
- [Publisher profile](https://clawhub.ai/user/zoucdr) <br>
- [WeryAI video CLI reference](resources/WERYAI_VIDEO_API.md) <br>
- [WeryAI video generation API](https://api.weryai.com) <br>
- [WeryAI model registry and upload API](https://api-growth-agent.weryai.com) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown response with expanded prompt details, JSON command examples, and playable video links when generation succeeds] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WERYAI_API_KEY, Node.js 18+, network access, and paid WeryAI usage; image inputs should be public HTTPS URLs unless the user explicitly consents to local upload.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
