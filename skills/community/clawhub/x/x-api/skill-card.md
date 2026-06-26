## Description: <br>
Post to X (Twitter) through the official API with OAuth 1.0a when reliable publishing is needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lobstergeneralintelligence](https://clawhub.ai/user/lobstergeneralintelligence) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to publish posts to X from an authorized account using official API credentials. It is intended for posting updates when cookie-based posting tools are unreliable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can directly publish posts from the user's X account and does not include a built-in confirmation step. <br>
Mitigation: Review every post text before running the command and install the skill only for agents that should be able to publish to X. <br>
Risk: X API credentials could be misused if tokens or local config files are exposed. <br>
Mitigation: Keep tokens in a locked-down secrets location, avoid committing credential files, and remove unexpected .x-api.json files from project directories. <br>
Risk: The npm dependency is version-ranged, so future installs may resolve to a newer package release. <br>
Mitigation: Pin and review the twitter-api-v2 dependency before deployment in controlled environments. <br>


## Reference(s): <br>
- [X Developer Portal](https://developer.x.com/en/portal/dashboard) <br>
- [X Developer Platform](https://developer.x.com) <br>
- [bird CLI](https://github.com/steipete/bird) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration] <br>
**Output Format:** [Plain text status output and tweet URL; setup guidance as Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires X API credentials and tweet text supplied by the user or agent.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
