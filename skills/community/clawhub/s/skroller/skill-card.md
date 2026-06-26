## Description: <br>
Automates collection, filtering, deduplication, digest generation, and export of public social media posts across platforms including Twitter/X, Instagram, TikTok, Reddit, LinkedIn, YouTube, Product Hunt, Medium, GitHub, and Pinterest. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[10OSS](https://clawhub.ai/user/10OSS) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and research teams use Skroller to gather public social media posts, filter them by query and engagement, generate digests, and export results to files or note-taking tools. Users should review platform terms, privacy obligations, and security guidance before collecting or storing data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad social-media scraping can conflict with platform terms, privacy law, or user consent expectations. <br>
Mitigation: Prefer official APIs where possible, review platform terms and robots.txt before use, limit collection to permitted public data, and document a lawful basis for any personal-data processing. <br>
Risk: Credential and session handling for authenticated platforms can expose cookies, API keys, or access tokens. <br>
Mitigation: Treat cookies and API tokens as secrets, keep them out of repositories and shared logs, store them in environment variables or a secret manager, and rotate them if exposed. <br>
Risk: Anti-bot, proxy, or high-volume guidance can increase compliance and account-enforcement risk. <br>
Mitigation: Avoid anti-bot and proxy evasion patterns, keep request rates low, stop when blocked, and use official platform access paths for production or commercial workflows. <br>
Risk: Unsafe local export commands can execute shell-sensitive content when exporting untrusted scraped text to Bear or Apple Notes. <br>
Mitigation: Avoid Bear and Apple Notes export for untrusted scraped content until command construction is fixed, or use dry-run and safer file-based exports such as JSON, CSV, Markdown, or Obsidian. <br>


## Reference(s): <br>
- [Skroller Skill Source](SKILL.md) <br>
- [Selector Reference](assets/selector-reference.md) <br>
- [Platform Details](references/platform-details.md) <br>
- [Rate Limits and Best Practices](references/rate-limits.md) <br>
- [ClawHub skill page](https://clawhub.ai/10OSS/skroller) <br>
- [Publisher profile](https://clawhub.ai/user/10OSS) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON, CSV, Markdown, or note-app export files produced by the bundled scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write scraped post datasets, digest files, note exports, screenshots, and local deduplication state depending on selected command options.] <br>

## Skill Version(s): <br>
0.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
