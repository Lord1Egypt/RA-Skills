## Description: <br>
Automatically monitor RSS feeds and post to social media. Schedule content, generate posts with AI, and publish to Twitter/LinkedIn. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fly3094](https://clawhub.ai/user/fly3094) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to monitor RSS feeds, draft platform-specific social posts, and manage feed-based content sharing workflows for Twitter and LinkedIn. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence says the documentation overstates automatic social publishing while the script only prints drafts. <br>
Mitigation: Treat generated posts as drafts and verify any publishing workflow separately before relying on automatic posting. <br>
Risk: The security guidance warns against providing social-media credentials or scheduling unattended runs before controls are corrected. <br>
Mitigation: Do not provide production social-media credentials or run unattended schedules until approval controls, rate limits, and the publishing path are reviewed. <br>
Risk: The bundled script can mark feed items as handled after preparing drafts. <br>
Mitigation: Review local history behavior and keep backups or use a test data directory before running against important feeds. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/fly3094/rss-to-social) <br>
- [Publisher Profile](https://clawhub.ai/user/fly3094) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal text with configuration examples and generated social post drafts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated posts are intended for review before publishing; local history may be updated by the bundled script.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
