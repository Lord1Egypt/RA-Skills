## Description: <br>
Fetches full YouTube transcripts from YouTube URLs, channels, or batch configs using watch-page scraping and InnerTube fallback when simpler transcript tools fail. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ioridev](https://clawhub.ai/user/ioridev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to retrieve source transcript text from individual YouTube videos, recent channel videos, or configured channel batches before downstream analysis, translation, summarization, or extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts YouTube directly and invokes yt-dlp while fetching video metadata and transcripts. <br>
Mitigation: Run it only in environments where direct YouTube access and yt-dlp execution are acceptable, and review updates to yt-dlp before deployment. <br>
Risk: The skill installs and imports third-party Python packages. <br>
Mitigation: Pin or lock dependency versions for production use and review dependency updates before installing them. <br>
Risk: Generated JSON files can contain full transcripts that may include sensitive or copyrighted content from source videos. <br>
Mitigation: Choose an output path with appropriate access controls and handle transcript files according to the sensitivity of the source material. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ioridev/youtube-transcript-fetcher) <br>
- [Publisher profile](https://clawhub.ai/user/ioridev) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Example channel configuration](artifact/config/channels.example.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration] <br>
**Output Format:** [JSON file containing per-video metadata, transcript text, extraction status, and aggregate stats] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes full transcript text to a configurable output path; defaults to /tmp/youtube_transcript_fetcher.json.] <br>

## Skill Version(s): <br>
0.1.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
