## Description: <br>
Viral Reels Creator helps agents create and edit vertical short-form videos for Instagram Reels, TikTok, and YouTube Shorts using ffmpeg workflows for scene detection, beat sync, captions, color grading, transitions, and multi-platform export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yash-kavaiya](https://clawhub.ai/user/yash-kavaiya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, marketers, and developers use this skill to turn uploaded video, image, and audio assets into polished vertical short-form videos and platform-specific exports. It helps plan viral hooks, generate ffmpeg commands, run helper scripts for scene and beat detection, and prepare final reels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may change the runtime environment by installing system and Python packages. <br>
Mitigation: Run it in an isolated workspace or container and confirm package installation before executing setup commands. <br>
Risk: Shell-based ffmpeg examples could execute unintended commands if crafted filenames are interpolated unsafely. <br>
Mitigation: Review generated commands, avoid untrusted filenames, and prefer subprocess argument lists or safely quoted arguments. <br>
Risk: The skill processes local uploaded media and creates video exports. <br>
Mitigation: Use only media the user is permitted to process and keep generated outputs in the configured workspace or output directory. <br>


## Reference(s): <br>
- [Viral Hooks](references/viral-hooks.md) <br>
- [Beat-Synced Editing](references/beat-sync.md) <br>
- [Platform Specs](references/platform-specs.md) <br>
- [Caption Templates](references/caption-templates.md) <br>
- [Animations](references/animations.md) <br>
- [Color Grading](references/color-grading.md) <br>
- [Transitions](references/transitions.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with ffmpeg, bash, and Python snippets plus generated video file paths when media is processed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce MP4 video exports and platform variants through ffmpeg and bundled helper scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
