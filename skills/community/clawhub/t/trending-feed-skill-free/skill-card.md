## Description: <br>
Fetches GitHub Trending repository lists with language filtering and returns structured JSON with repository descriptions, star counts, and primary languages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical leads, analysts, and content creators use this skill to collect current GitHub Trending repositories for daily review, language ecosystem tracking, reports, and lightweight trend analysis. It is not intended for real-time streaming analytics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to run local Python commands and fetch public GitHub data. <br>
Mitigation: Review proposed shell commands before execution and run them in an environment where network access to GitHub is acceptable. <br>
Risk: Broad save and export behavior could overwrite local files if paths are not chosen deliberately. <br>
Mitigation: Specify output paths explicitly, avoid existing filenames unless replacement is intended, and inspect generated JSON before reuse. <br>
Risk: Providing a GitHub token increases credential exposure if it is unnecessary for the task. <br>
Mitigation: Use unauthenticated public requests by default and provide a token only when higher API limits are required. <br>
Risk: Generated Trending data can be incomplete, stale, rate-limited, or affected by network errors. <br>
Mitigation: Check logs and result counts, retry later when rate-limited, and validate important repository details against GitHub before making decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/trending-feed-skill-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>
- [Skill homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and structured JSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include repository full name, description, language, star count, and URL; agents may format results for chat, console, or saved JSON files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
