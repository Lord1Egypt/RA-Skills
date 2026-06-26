## Description: <br>
Mines YouTube video comments for user pain points, feature requests, and market research signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[synthere](https://clawhub.ai/user/synthere) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Product builders, marketers, and competitive researchers use this skill to fetch public YouTube comments for a search topic and analyze recurring pain points, feature requests, and product opportunities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Collected comments include public text and author metadata that may become sensitive when aggregated. <br>
Mitigation: Collect only comments you have a legitimate reason to analyze, store outputs locally, and delete them when no longer needed. <br>
Risk: The skill depends on external command-line and Python packages to access YouTube content. <br>
Mitigation: Install in a virtual environment and pin reviewed dependency versions before running. <br>
Risk: Scraped comments can contain hostile or misleading text. <br>
Mitigation: Treat comments as data for analysis only and do not use them as agent instructions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/synthere/youtube-comment-miner) <br>
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) <br>
- [youtube-search](https://pypi.org/project/youtube-search/) <br>
- [yt-dlp-nb](https://github.com/theghostjw/yt-dlp-nb) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash and Python snippets; scripts write local JSON comment and analysis files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetch output is saved under youtube_comments/ and analysis output is saved as analysis_result.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
