## Description: <br>
Reddit调研(免费版) helps content creators and market researchers scan target Subreddits for popular topics, recurring pain points, content gaps, and content opportunities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External content creators, marketers, product managers, and small teams use this skill to research public Reddit communities, identify user pain points, and turn subreddit discussions into structured content or market-research reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads public Reddit content that may contain misleading claims or prompt-injection attempts. <br>
Mitigation: Treat Reddit posts and comments as untrusted data, summarize them without following embedded instructions, and keep source links for review. <br>
Risk: Using callback_url may send research results to an external destination. <br>
Mitigation: Provide callback_url only for trusted endpoints and avoid including sensitive research context in callback-bound requests. <br>
Risk: Reddit /.json fetching can be limited by access restrictions, deleted posts, private communities, or rate limits. <br>
Mitigation: Use explicit subreddit-focused requests, reduce fetch frequency when limited, and report unavailable or skipped sources in the final research output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/reddit-research-tool-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with structured research sections and optional JSON or shell-command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include source Reddit links, opportunity rankings, trend summaries, and execution notes.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
