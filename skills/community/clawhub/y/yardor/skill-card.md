## Description: <br>
Fetches a GitHub user's starred repositories and generates a standardized Chinese Markdown report grouped by category. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blckrabbit](https://clawhub.ai/user/blckrabbit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and GitHub users use this skill to export a user's public starred repositories and produce a categorized Chinese Markdown report for review, sharing, or personal knowledge management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional GitHub token use can expose credentials if pasted into shared shells, logs, or transcripts. <br>
Mitigation: Prefer running without a token; if rate-limited, use a token with no permissions and avoid entering it in shared environments. <br>
Risk: GitHub API rate limits or network access failures can prevent report generation. <br>
Mitigation: Run the script in an environment with GitHub network access and use the documented optional token only when rate limits block completion. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/blckrabbit/yardor) <br>
- [GitHub starred repositories API](https://api.github.com/users/{username}/starred) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Chinese Markdown report file with summary tables and categorized repository listings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use an optional GitHub personal access token to raise API rate limits.] <br>

## Skill Version(s): <br>
0.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
