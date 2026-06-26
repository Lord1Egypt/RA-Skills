## Description: <br>
Generates a cybersecurity daily digest from CyberSecurityRSS OPML feeds and Twitter/X security KOL accounts, with provider selection, recent-window filtering, archive deduplication, vulnerability merging, source health monitoring, and Markdown output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zer0yu](https://clawhub.ai/user/zer0yu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Security researchers and engineers use this skill to fetch recent security and AI-related items from RSS and Twitter/X sources, score and deduplicate them, merge vulnerability events, and generate a bilingual Markdown digest. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches public internet sources and stores local digest state. <br>
Mitigation: Review configured RSS and Twitter/X sources before use and keep state in an approved local directory. <br>
Risk: Collected content may be sent to the selected AI provider during scoring and summarization. <br>
Mitigation: Use --dry-run, --no-twitter, or the Ollama provider when lower external exposure is required. <br>
Risk: Optional email delivery can distribute digest content outside the local environment. <br>
Mitigation: Use --email only with an approved mail account and recipient. <br>


## Reference(s): <br>
- [Digest prompt templates](references/digest-prompt.md) <br>
- [Sec Daily Digest on ClawHub](https://clawhub.ai/zer0yu/sec-daily-digest) <br>
- [twitterapi.io](https://twitterapi.io) <br>
- [gogcli](https://github.com/steipete/gogcli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Bilingual Markdown digest with optional command and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can use dry-run mode, provider selection, optional Twitter/X fetching, optional full-text enrichment, and optional email delivery.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release metadata; artifact frontmatter lists 0.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
