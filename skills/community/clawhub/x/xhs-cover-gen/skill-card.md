## Description: <br>
Generates Xiaohongshu (RED) cover images with Chinese text overlays using split, gradient, or card layouts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huuuwnnn-droid](https://clawhub.ai/user/huuuwnnn-droid) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators and agents use this skill to generate 3:4 Xiaohongshu cover images with Chinese titles, subtitles, labels, and optional AI-generated backgrounds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send base-image prompt text to Pollinations.ai. <br>
Mitigation: Do not include private, proprietary, or personal information in base prompts unless that external disclosure is acceptable. <br>
Risk: The skill may make runtime network calls, download a font, cache files in /tmp, and write a JPEG to the requested output path. <br>
Mitigation: Run it only in environments where that network access, temporary caching, and output-file write behavior are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huuuwnnn-droid/xhs-cover-gen) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [JPEG image file with command-line status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default output is a 1080x1440 JPEG at 95% quality; dimensions, style, colors, labels, text, and output path are configurable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
