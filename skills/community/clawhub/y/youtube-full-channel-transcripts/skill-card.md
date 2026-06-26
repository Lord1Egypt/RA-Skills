## Description: <br>
Extract transcripts from all videos in a YouTube channel for free, using yt-dlp to discover videos, fetch available subtitles, and save combined transcripts as structured JSON or CSV. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[otomazeli](https://clawhub.ai/user/otomazeli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and content operators use this skill to collect subtitles from a YouTube channel or playlist and export them as JSON or CSV transcript datasets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running local yt-dlp and jq against YouTube may process many videos and depend on locally installed command-line tools. <br>
Mitigation: Use trusted installations of yt-dlp and jq, and set max_videos for large channels. <br>
Risk: The skill writes transcript exports to output_dir and clears an existing transcripts.json or transcripts.csv in that directory. <br>
Mitigation: Choose output_dir intentionally and avoid pointing it at a directory containing transcript exports you need to preserve. <br>
Risk: Large channels can take a long time and may encounter rate limits or missing transcripts. <br>
Mitigation: Use max_videos and language filters, and expect videos without available subtitles to be skipped. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/otomazeli/youtube-full-channel-transcripts) <br>
- [yt-dlp project](https://github.com/yt-dlp/yt-dlp) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, CSV, shell commands] <br>
**Output Format:** [Transcript export files in JSON Lines or CSV with a console summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes transcripts.json or transcripts.csv to the configured output_dir.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
