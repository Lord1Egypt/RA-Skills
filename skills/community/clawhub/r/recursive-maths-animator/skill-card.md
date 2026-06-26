## Description: <br>
Recursive maths animator helps agents plan, implement, render, and verify Manim-based mathematical and data animations with optional voiceover, reusable design systems, pattern libraries, and git-backed scene versioning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[science-prof-robot](https://clawhub.ai/user/science-prof-robot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, educators, and content teams use this skill to turn mathematical explanations, statistical concepts, and business data into shareable Manim animations with planned story beats, visual themes, rendered previews, and verification feedback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud voiceover features can send narration text to third-party services such as gTTS or Gemini. <br>
Mitigation: Do not use sensitive, proprietary, or regulated narration text with cloud voiceover providers unless their terms and data handling have been reviewed. <br>
Risk: Gemini voiceover use requires a sensitive credential. <br>
Mitigation: Use environment-based credential handling for GEMINI_API_KEY and avoid committing keys or generated configuration containing secrets. <br>
Risk: The Manim and ffmpeg workflow writes project files, rendered media, and verification artifacts locally. <br>
Mitigation: Run the workflow in an intended project directory and review generated files before sharing or publishing outputs. <br>
Risk: Copy-based installation can overwrite files in an existing destination. <br>
Mitigation: Check the destination directory before copying skill files and preserve any local files that should not be replaced. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/science-prof-robot/recursive-maths-animator) <br>
- [Manim guide](artifact/references/manim_guide.md) <br>
- [Video verification rubric](artifact/references/video_verification_rubric.md) <br>
- [Manim project versioning helper](artifact/references/manim_versioning.py) <br>
- [Pattern library](artifact/references/pattern_library/) <br>
- [Pipeline runner](artifact/scripts/run_pipeline.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation of local Manim project files, verification artifacts, and MP4 or GIF render outputs.] <br>

## Skill Version(s): <br>
1.7.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
