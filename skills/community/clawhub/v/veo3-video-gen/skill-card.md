## Description: <br>
Generate and stitch short videos via Google Veo 3.x using the Gemini API (google-genai). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bluelyw](https://clawhub.ai/user/bluelyw) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to generate short MP4 video clips from text prompts or reference images via Google Veo 3.x, and to stitch multiple segments into longer videos with ffmpeg. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Gemini API keys can be exposed if passed on the command line. <br>
Mitigation: Prefer a restricted key supplied through GEMINI_API_KEY instead of --api-key. <br>
Risk: Multiple segments trigger multiple Veo requests and can increase quota or billing usage. <br>
Mitigation: Confirm the requested segment count before running generation. <br>
Risk: Prompts and reference images are sent to Gemini for generation. <br>
Mitigation: Do not submit sensitive prompts or reference images unless that disclosure is intended. <br>
Risk: Generated output and ffmpeg operations can overwrite existing files. <br>
Mitigation: Choose output filenames deliberately and check paths before execution. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown with inline bash command examples and MP4 file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Gemini API key; multi-segment output requires ffmpeg and may overwrite existing output files.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
