## Description: <br>
Video Slicer helps an agent turn long videos into topic-based short clips by sampling frames, transcribing audio with local Whisper, planning segments, and cutting media with ffmpeg. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abill6688](https://clawhub.ai/user/abill6688) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, educators, meeting teams, and developers use this skill to extract coherent short clips from long lectures, meetings, interviews, livestreams, or course recordings. It supports frame review, local Chinese transcription, clip planning, and ffmpeg-based media cutting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided videos, generated frames, extracted audio, transcripts, and clips may contain sensitive content. <br>
Mitigation: Run the skill only on videos the user has permission to process and treat all generated media and transcript artifacts as sensitive when the source video is sensitive. <br>
Risk: The skill runs local ffmpeg and Python processing that writes media files to disk. <br>
Mitigation: Install and run it in an isolated Python environment, review output paths before execution, and use a dedicated output directory. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/abill6688/video-slicer) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [video_slicer.py](artifact/scripts/video_slicer.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with bash and Python snippets, JSON clip plans, transcript files, sampled frames, and generated MP4 clips.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local ffmpeg and Python. The workflow writes frames, extracted audio, transcripts, clip plans, and videos under a user-selected output directory.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter, README, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
