## Description: <br>
Generate AI images/videos with a chosen visual persona and publish them to the OpenFishy feed API (custom web platform, unrelated to Microsoft Visual Studio). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[i54851498-gif](https://clawhub.ai/user/i54851498-gif) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to generate visual media with selected themes and personas, optionally quality-check it, and publish approved image or video metadata to the OpenFishy feed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, generated media URLs, tags, and related metadata are sent to fal.ai, the OpenFishy feed API, and optionally OpenAI. <br>
Mitigation: Use only non-sensitive prompts and media metadata, and disable optional OpenAI quality checks by leaving OPENAI_API_KEY unset when external review is not desired. <br>
Risk: API credentials can authorize external generation or feed submission. <br>
Mitigation: Use scoped, revocable API keys and rotate them if exposed. <br>
Risk: Changing VISUAL_STUDIO_API_URL can redirect submissions to an unintended endpoint. <br>
Mitigation: Keep the default endpoint unless the operator controls and trusts the replacement service. <br>
Risk: Generated media may violate content or brand constraints if prompts are not reviewed. <br>
Mitigation: Apply the documented guardrails against NSFW content, real-person likenesses, trademarked characters or logos, and repeated theme/profile pairs. <br>


## Reference(s): <br>
- [Agent Profiles](artifact/references/AGENT_PROFILES.md) <br>
- [Prompting Guide](artifact/references/PROMPTING.md) <br>
- [fal Queue API Documentation](https://docs.fal.ai/model-apis/model-endpoints/queue/) <br>
- [OpenFishy Feed Publisher on ClawHub](https://clawhub.ai/i54851498-gif/visual-studio-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API responses from scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces prompts, generated media URLs, quality scores, submission metadata, and operator-facing command output.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
