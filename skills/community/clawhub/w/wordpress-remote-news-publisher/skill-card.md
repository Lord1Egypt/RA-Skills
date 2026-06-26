## Description: <br>
Automates news article creation and publishing to a remote WordPress site via SSH and WP-CLI, including cover image handling and Yoast SEO metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[promoweb](https://clawhub.ai/user/promoweb) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, editors, and site operators use this skill to generate sourced news articles, prepare cover images, and publish posts to a remote WordPress installation with SEO metadata. It is intended for teams that control the target WordPress server and can review content before it goes live. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish to a live WordPress site over SSH. <br>
Mitigation: Keep publishing in draft or manual-review mode until the generated article, sources, image, and SEO metadata are approved. <br>
Risk: SSH access and host verification choices can expose the target server if used carelessly. <br>
Mitigation: Use a dedicated low-privilege SSH key and user, avoid root or admin SSH access, and pin or verify the SSH host key before production use. <br>
Risk: Shared temporary files can mix state between runs or expose article and media identifiers on multi-user systems. <br>
Mitigation: Replace shared /tmp state files with per-run private files before production scheduling. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/promoweb/wordpress-remote-news-publisher) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with JSON article data and shell command invocations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates article, media, and post state through local temporary files and remote WordPress operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact/config.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
