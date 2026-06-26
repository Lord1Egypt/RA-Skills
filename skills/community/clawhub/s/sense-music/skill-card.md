## Description: <br>
Music perception for AI entities - hear BPM, key, structure, genre, mood, and lyrics in audio files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vveerrgg](https://clawhub.ai/user/vveerrgg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to analyze local or URL-based audio and return musical observations such as tempo, key, structure, genre, mood, lyrics, summaries, and visualizations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a Python package plus audio and ML dependencies. <br>
Mitigation: Install it only in environments where those package and dependency risks are acceptable, and review dependency updates before deployment. <br>
Risk: Audio analysis can produce transcripts, HTML, JSON, and image exports that may contain private speech, personal information, or copyrighted content. <br>
Mitigation: Analyze only audio files or URLs you have permission to process, then review, restrict, or delete generated exports when they contain sensitive material. <br>
Risk: URL-based audio analysis retrieves remote content. <br>
Mitigation: Use trusted URLs and rely on the skill's documented private, loopback, and link-local URL blocking as part of normal network-safety review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vveerrgg/sense-music) <br>
- [OpenClaw homepage](https://github.com/HumanjavaEnterprises/huje.sensemusic.OC-python.src) <br>
- [PyPI package](https://pypi.org/project/sense-music/) <br>
- [huje.tools](https://huje.tools) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, html, image files, guidance] <br>
**Output Format:** [Structured analysis objects with natural-language summaries, optional lyrics, JSON or HTML exports, and generated spectrogram or waveform images.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ffmpeg and the sense-music Python package; Whisper models may be downloaded and cached on first use.] <br>

## Skill Version(s): <br>
0.1.5 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
