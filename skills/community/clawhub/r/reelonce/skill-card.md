## Description: <br>
ReelOnce orchestrates a text-to-video workflow from story planning through asset images, storyboard images, TTS, shot video generation, Remotion project creation, and final MP4 rendering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pampas-lab](https://clawhub.ai/user/pampas-lab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and video workflow teams use this skill to turn story text into a generated ReelOnce project, supporting assets, shot videos, a Remotion React project, and an optional final MP4 render. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: External generation services may receive story text, prompts, reference images, or generated media inputs. <br>
Mitigation: Use a trusted configured video provider and avoid sensitive local images or story material unless that provider and workflow are acceptable for the data. <br>
Risk: Normal use can install and run Remotion and npm rendering dependencies inside the generated project. <br>
Mitigation: Install only in a trusted ReelOnce repository and inspect the generated Remotion project before full rendering when dependency execution matters. <br>
Risk: API keys and environment configuration are required for video generation. <br>
Mitigation: Keep env.local and API keys private, and load only the environment variables needed for the current run. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pampas-lab/reelonce) <br>
- [Primary skill documentation](artifact/SKILL.md) <br>
- [ReelOnce workflow reference](artifact/references/README.md) <br>
- [skills.video](https://skills.video/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Configuration, Files, Video, Guidance] <br>
**Output Format:** [JSON status output plus generated project files, media assets, a Remotion React project, and optional MP4 video output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports project IDs, shot counts, reference-image source selection, debug prompt export, no-render mode, subtitle control, partial-result continuation, and machine-readable JSON output.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
