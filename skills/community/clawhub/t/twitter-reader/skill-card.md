## Description: <br>
Extracts public X/Twitter tweet and thread data from URLs, including text, author details, timestamps, engagement metrics, media links, quoted tweets, and thread context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iheardulkBTC](https://clawhub.ai/user/iheardulkBTC) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Agents and developers use this skill to read, summarize, analyze, or extract structured data from public X/Twitter tweet URLs and same-author threads. It is useful for content review, research workflows, journalism, social media monitoring, and automation that needs tweet metadata or media references. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tweet lookup URLs are sent to third-party services, which can reveal which public tweet was requested. <br>
Mitigation: Avoid using this skill for lookups where the requested tweet URL should remain private from FxTwitter or public Nitter instances. <br>
Risk: The Nitter fallback depends on public instances that may be unavailable or unreliable. <br>
Mitigation: Prefer the FxTwitter-based reader and treat Nitter results as best-effort fallback output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/iheardulkBTC/twitter-reader) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Script output includes success/error status, tweet text, author metadata, timestamps, engagement counts, media URLs, quote tweet data, source service, and fetch time when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
