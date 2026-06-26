## Description: <br>
A local audio separation skill that helps users split audio or video into vocals, accompaniment, drums, bass, piano, and other stems, with preview, download, trimming, history, and REST API workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nabian1990amber-cmd](https://clawhub.ai/user/nabian1990amber-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, creators, podcasters, music educators, and developers use this skill to run a local media-processing web tool for separating audio or video into stems, previewing results, downloading MP3 tracks, trimming segments, and calling the same workflow through REST endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local unauthenticated web API can expose, trim, download, and delete processed media while the service is running. <br>
Mitigation: Keep the service bound to localhost, stop it when not in use, avoid browsing untrusted sites while it is running, and manually manage or delete sensitive uploads, outputs, trims, and history. <br>
Risk: The workflow processes local audio and video files and stores uploads, generated stems, trims, and history on disk. <br>
Mitigation: Use non-sensitive media when possible and clear generated files and history after processing sensitive content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nabian1990amber-cmd/sound-split) <br>
- [Demucs project](https://github.com/facebookresearch/demucs) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration, Files] <br>
**Output Format:** [Markdown with setup commands, REST API descriptions, and bundled FastAPI and HTML source files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The local tool produces downloadable MP3 stem files and trimmed audio segments from uploaded media.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
