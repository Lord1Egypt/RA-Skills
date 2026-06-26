## Description: <br>
AI song and music generator that helps agents create songs with vocals, instrumentals, beats, and lyrics from natural-language descriptions using the Mureka API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gxcun17](https://clawhub.ai/user/gxcun17) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agent operators use this skill to turn natural-language music ideas into structured prompts, lyrics, Mureka CLI commands, and locally saved generated audio outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, lyrics, and requested audio uploads are sent to Mureka for generation. <br>
Mitigation: Use the skill only with material you are comfortable sending to Mureka, and avoid submitting sensitive or unlicensed audio. <br>
Risk: Mureka usage depends on a user-managed API key and may incur account billing. <br>
Mitigation: Use a dedicated MUREKA_API_KEY, monitor account usage, and confirm balance before large generation runs. <br>
Risk: Translated or inferred music prompts may not match the user's intended meaning. <br>
Mitigation: Review the structured prompt before generation, especially when the original request is multilingual or culturally specific. <br>
Risk: Reference tracks and vocal samples can raise consent or rights issues. <br>
Mitigation: Only upload audio that the user has permission to process, and confirm consent for vocal cloning inputs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gxcun17/skywork-music-maker) <br>
- [Music Prompt Crafting Guide](references/prompt_guide.md) <br>
- [Mureka API endpoint](https://api.mureka.ai) <br>
- [Mureka platform](https://platform.mureka.ai) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, text] <br>
**Output Format:** [Markdown guidance with inline bash commands and locally saved audio and lyrics files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MUREKA_API_KEY and Python 3 with requests; generated audio is saved to a user-selected output directory.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
