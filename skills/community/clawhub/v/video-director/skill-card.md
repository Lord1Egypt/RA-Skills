## Description: <br>
Video Director plans knowledge-focused short-video visuals by turning scripts into structured storyboard JSON with noun visualization and entrance-animation guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a1024708231](https://clawhub.ai/user/a1024708231) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, developers, and content teams use this skill to convert knowledge or explainer scripts into vertical short-video scene plans, including visual elements, animation timing, duration estimates, and handoff-ready storyboard JSON for downstream video production. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Default output behavior may add a ClawHub-branded ending. <br>
Mitigation: Review the final scene before publishing and provide custom endingText, endingTitle, and endingDesc values when neutral or client-specific copy is required. <br>
Risk: Generated storyboard choices can be visually persuasive but may not match the user's intended message or brand constraints. <br>
Mitigation: Review scene text, visual prompts, timing, and animation choices before rendering or publishing a video. <br>
Risk: The local Node script reads intended input files and can write an output JSON file. <br>
Mitigation: Run the script only with expected input and output paths in a controlled workspace. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Markdown, Guidance] <br>
**Output Format:** [Structured storyboard JSON; optionally a Markdown scene-planning table] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Targets 9:16 vertical video at 1080x1920 and 30 FPS, with scene timing, visual elements, animation metadata, and configurable ending text.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
