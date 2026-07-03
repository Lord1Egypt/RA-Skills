## Description: <br>
Deep-crawls websites from one or more start URLs and returns per-page LLM-ready text, markdown, or HTML with metadata and in-scope links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[browseract-cli](https://clawhub.ai/user/browseract-cli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data teams, and agents use this skill to build clean website corpora for RAG pipelines, knowledge bases, vector databases, chatbot knowledge files, or documentation synchronization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The crawler can use an active browser session and may capture authenticated pages. <br>
Mitigation: Use it only on sites you own or are allowed to crawl, avoid logged-in sessions unless necessary, and review captured pages before sharing or indexing. <br>
Risk: The skill writes crawled content and crawl state to disk, which may persist sensitive page content. <br>
Mitigation: Choose a controlled output directory, set tight scope limits, and delete or protect generated files that contain sensitive content. <br>
Risk: Server security guidance flags rate-limit evasion concerns around stealth multi-session use. <br>
Mitigation: Do not use stealth multi-session behavior to bypass site controls; use polite delays and explicit page, depth, and glob limits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/browseract-cli/skills/webcrawler-deep-crawl) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Markdown, Text, HTML, Files, Shell commands, Guidance] <br>
**Output Format:** [Per-page JSON records with optional markdown, text, or HTML bodies plus crawl metadata, outbound links, crawl state, and a summary.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes page records and crawl state to disk; supports page limits, depth limits, include/exclude URL globs, content selectors, and optional JSONL concatenation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
