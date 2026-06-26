## Description: <br>
Adds post-production overlays to existing video clips, including AI cover frames, HTML/CSS captions, timed illustrations, chapter chips, and CTA scenes, then guides HyperFrames rendering to an upload-ready MP4. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jianshuo](https://clawhub.ai/user/jianshuo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and video-production agents use this skill after clipping or segmenting a source video to add covers, captions, timed motion graphics, illustration overlays, and closing CTA scenes. It is most useful when the desired output is a polished MP4 rendered through a single HyperFrames composition rather than a cascade of re-encodes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Custom overlay fragments are treated as high-trust code execution because they can inline HTML, CSS, and JavaScript into the generated composition. <br>
Mitigation: Use custom fragments only from trusted sources, review generated overlay code before rendering, and run the renderer in a sandbox without access to sensitive files, credentials, or private network resources. <br>
Risk: Generated projects may execute local render and package commands while producing video outputs. <br>
Mitigation: Review the generated project files and commands, run HyperFrames lint/validate/inspect before render, and execute the workflow in a controlled working directory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jianshuo/wjs-overlaying-video) <br>
- [custom_overlay_recipes.md](references/custom_overlay_recipes.md) <br>
- [illustration_patterns.md](references/illustration_patterns.md) <br>
- [build_hf_clips.py](references/build_hf_clips.py) <br>
- [illustrations.py](references/illustrations.py) <br>
- [example_spec.json](references/example_spec.json) <br>
- [GSAP distribution used by generated compositions](https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with JSON specs, HTML/CSS/JavaScript fragments, Python commands, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces HyperFrames project scaffolding and render commands; the final media artifact is an upload-ready MP4 generated outside the agent response.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
