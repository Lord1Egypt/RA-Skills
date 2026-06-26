## Description: <br>
Fetches YouTube transcripts through the Apify API with local caching, batch mode, language preference support, and text or JSON output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[robbyczgw-cla](https://clawhub.ai/user/robbyczgw-cla) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agents, and external users use this skill to retrieve YouTube transcripts through Apify when direct YouTube transcript access may fail from cloud networks, then use the transcript text or JSON for summarization, analysis, or batch processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: YouTube video URLs are sent to Apify, and an Apify token may spend account quota. <br>
Mitigation: Use a dedicated Apify token, submit only intended YouTube transcript requests, and monitor Apify billing or usage limits. <br>
Risk: Local transcript caching can retain transcript content and video history on disk. <br>
Mitigation: Choose an appropriate cache directory for the work, disable fresh caching when needed, and clear cached transcripts when history should not be retained. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/robbyczgw-cla/youtube-apify-transcript) <br>
- [Apify pricing](https://apify.com/pricing) <br>
- [Apify API token setup](https://console.apify.com/account/integrations) <br>
- [YouTube Transcript Scraper actor](https://apify.com/topaz_sharingan/Youtube-Transcript-Scraper-1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Shell commands, Guidance] <br>
**Output Format:** [Plain text transcripts or JSON with metadata and timestamped segments; optional transcript files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports single-video and batch URL input, language preference, optional output files, and local transcript caching.] <br>

## Skill Version(s): <br>
1.3.3 (source: frontmatter, package.json, CHANGELOG released 2026-03-31, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
