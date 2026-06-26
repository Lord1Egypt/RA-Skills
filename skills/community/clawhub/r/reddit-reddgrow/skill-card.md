## Description: <br>
Reddit intelligence CLI for AI agents. Use when working with reddit posts, subreddit research, comments, user profiles, wiki pages, domain mentions, marketing, community rules, or URL checking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yahavf6](https://clawhub.ai/user/yahavf6) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agent operators use this skill to query Reddit-related information through the ReddGrow CLI, including subreddit research, post and comment lookup, user profile review, domain mention monitoring, and posting-readiness checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Subreddit names, usernames, domains, URLs, post IDs, and search queries may be sent to ReddGrow during CLI use. <br>
Mitigation: Avoid sensitive internal targets unless approved, and install only if the ReddGrow service and @reddgrow/cli package are trusted. <br>
Risk: Large batches can consume API credits or expose more query metadata than intended. <br>
Mitigation: Check authentication and credit status before larger operations, monitor API key usage, and scope batch inputs deliberately. <br>
Risk: Reddit posting workflows can violate community rules if checks are skipped. <br>
Mitigation: Use the documented rules, wiki, subreddit type, submission type, and duplicate URL checks before posting or sharing links. <br>


## Reference(s): <br>
- [ReddGrow homepage](https://reddgrow.ai) <br>
- [ClawHub skill page](https://clawhub.ai/yahavf6/reddit-reddgrow) <br>
- [Publisher profile](https://clawhub.ai/user/yahavf6) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON CLI output descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands expect the reddgrow binary and REDDGROW_API_KEY; ReddGrow CLI commands return JSON to stdout.] <br>

## Skill Version(s): <br>
0.1.6 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
