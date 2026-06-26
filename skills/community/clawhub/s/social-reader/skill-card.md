## Description: <br>
Social media content scraping and automation skill. Supports real-time single post reading, as well as scheduled batch patrol, LLM distillation, and review notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HackSing](https://clawhub.ai/user/HackSing) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to fetch social media posts for discussion or reply drafting, and to run a batch pipeline that collects posts, generates LLM-assisted commentary drafts, and presents them for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tweet targets and fetched content may be sent to third-party fetch providers and the configured LLM provider. <br>
Mitigation: Use the skill only with content you are comfortable sharing with those services, and configure a limited LLM API key for pipeline processing. <br>
Risk: Pipeline review mode starts an unauthenticated local review server. <br>
Mitigation: Run review mode only on a trusted machine and add strict URL allow-listing, authentication, or CSRF protection before regular use. <br>
Risk: The local review server exposes draft review and regeneration actions while it is running. <br>
Mitigation: Avoid browsing untrusted sites while the server is active and shut the review server down when review work is complete. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/HackSing/social-reader) <br>
- [Publisher profile](https://clawhub.ai/user/HackSing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON fetch results, Markdown-formatted article text, generated commentary drafts, review UI content, and command-line status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Interactive fetches return structured post or article content; pipeline mode writes queue, draft, archive, and deduplication JSON files.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
