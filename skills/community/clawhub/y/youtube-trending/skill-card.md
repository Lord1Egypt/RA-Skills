## Description: <br>
Fetch and display the top trending YouTube videos globally or by country/category. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brunovu20](https://clawhub.ai/user/brunovu20) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to fetch current YouTube trending videos by region and category through the YouTube Data API, then present ranked results with engagement details and direct links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a YouTube Data API key and sends requests to Google's YouTube Data API. <br>
Mitigation: Use a restricted API key, keep it out of shared logs and source files, and only persist it in a shell profile when needed. <br>
Risk: Trending results depend on YouTube API availability, quota, region, category, and current ranking behavior. <br>
Mitigation: Treat results as live API output, handle quota or 403 errors, and avoid fabricating titles or view counts when the API fails. <br>


## Reference(s): <br>
- [YouTube Data API videos endpoint](https://www.googleapis.com/youtube/v3/videos) <br>
- [YouTube mostPopular videos API query](https://www.googleapis.com/youtube/v3/videos?chart=mostPopular) <br>
- [Google Cloud Console](https://console.cloud.google.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Terminal text output with Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3 and a YOUTUBE_API_KEY environment variable; supports optional region, count, and category arguments.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
