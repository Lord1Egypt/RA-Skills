## Description: <br>
Search and download licensed music from Trackyard's AI-powered catalog, including natural-language search, filtering, and optional clip trimming. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[benny-conn](https://clawhub.ai/user/benny-conn) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External creators, media teams, advertisers, podcasters, and developers use this skill to search for licensed background music, inspect track metadata, and download full or trimmed MP3 files for online content workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Trackyard API key and uses it to make authenticated API requests. <br>
Mitigation: Use a revocable API key, monitor credit usage, and avoid sharing logs or command output that may expose credentials. <br>
Risk: Download commands write MP3 files to the local working directory and may overwrite an existing file if the same output name is reused. <br>
Mitigation: Run downloads from a dedicated folder or pass an explicit output filename for each download. <br>


## Reference(s): <br>
- [Trackyard](https://trackyard.com) <br>
- [Trackyard ClawHub Skill](https://clawhub.ai/benny-conn/trackyard) <br>
- [Trackyard API Endpoint](https://api.trackyard.com/api/external/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Files] <br>
**Output Format:** [Shell commands that return JSON account, usage, and search data or save MP3 downloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and TRACKYARD_API_KEY; downloads write MP3 files locally and may consume Trackyard credits.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
