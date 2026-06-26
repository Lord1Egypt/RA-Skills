## Description: <br>
YouTube Analytics helps agents use the YouTube Data API v3 to analyze channels, videos, searches, subscriber counts, engagement metrics, uploads, and competitors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adamkristopher](https://clawhub.ai/user/adamkristopher) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to fetch public YouTube channel, video, and search data, save JSON results, and prepare markdown summaries with tables, comparisons, and performance insights. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a YouTube Data API key from the local environment. <br>
Mitigation: Use a restricted API key, avoid printing key values returned by helper functions, and rotate the key if it is exposed. <br>
Risk: The skill saves analysis results to local JSON files under results/. <br>
Mitigation: Install and run it only in workspaces where local result files are acceptable, and delete results/ when saved analyses are no longer needed. <br>
Risk: Dependency installation may change if package ranges resolve differently. <br>
Mitigation: Prefer lockfile-based installs such as npm ci when possible. <br>


## Reference(s): <br>
- [API Reference](references/api-reference.md) <br>
- [Google Cloud Console Credentials](https://console.cloud.google.com/apis/credentials) <br>
- [ClawHub Release Page](https://clawhub.ai/adamkristopher/youtube-analytics) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Analysis, JSON, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [JSON result files and markdown summaries, with TypeScript function calls and shell commands in setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a YouTube Data API v3 key and writes saved analyses under results/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and scripts/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
