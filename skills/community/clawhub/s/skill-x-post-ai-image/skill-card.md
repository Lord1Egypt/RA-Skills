## Description: <br>
Generate an AI image via Gemini and post it to X (Twitter) using OAuth1. Supports text-only or text+image tweets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zero2Ai-hub](https://clawhub.ai/user/Zero2Ai-hub) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and social media operators use this skill to generate Gemini images and publish text-only or text-plus-image posts to X/Twitter from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish live X/Twitter posts using OAuth tokens. <br>
Mitigation: Use a test or dedicated X/Twitter account where possible and review tweet text and image prompts before execution. <br>
Risk: The image helper path can be overridden with NANO_BANANA_SCRIPT and runs with broad environment access. <br>
Mitigation: Use only a trusted helper script, avoid untrusted NANO_BANANA_SCRIPT values, and isolate credentials so image generation cannot access posting tokens. <br>
Risk: Runtime credentials include X/Twitter OAuth tokens and a Gemini API key. <br>
Mitigation: Set credentials only in a controlled environment and avoid sharing them with unrelated tools or shells. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Zero2Ai-hub/skill-x-post-ai-image) <br>
- [Zero2Ai-hub publisher profile](https://clawhub.ai/user/Zero2Ai-hub) <br>
- [X/Twitter media upload endpoint used by the skill](https://upload.twitter.com/1.1/media/upload.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, API Calls] <br>
**Output Format:** [Markdown instructions and command examples; runtime stdout logs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can generate a PNG, resize it to a JPEG media attachment, upload it to X/Twitter, and post tweet text with an optional media ID.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
